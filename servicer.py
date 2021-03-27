from bs4 import BeautifulSoup
import re
import requests
from functools import lru_cache

APACHE = 1
OPENSSH = 2

name_map = {
    APACHE: 'Apache',
    OPENSSH: 'OpenSSH'
}


def check_output(input_string):
    if input_string is None:
        return (None, 0)
    if "Server: Apache/" in input_string:
        return (APACHE, input_string.split("Server: Apache/", 1)[1].split(" ", 1)[0])
    if "OpenSSH_" in input_string:
        return (OPENSSH, input_string.split("OpenSSH_", 1)[1].split(" ", 1)[0][:3])
    return None


def get_service_name(service_id):
    if service_id in name_map:
        return name_map[service_id]
    return "Unknown service"


# Get current Apache version
def get_version_apache():
    page = requests.get("https://github.com/apache/httpd/releases")
    soup = BeautifulSoup(page.content, 'html.parser')
    release_tags = soup.find_all(
        "div", class_="release-timeline-tags release-entry")[0]
    items = release_tags.find_all(class_="commit-title")
    tonight = items[0].findChildren("a", recursive=False)[0]
    invalid_tags = ['svg', 'path', 'u']
    for tag in invalid_tags:
        for match in tonight.findAll(tag):
            match.replaceWithChildren()
    s = str(tonight.contents)
    version_apache = re.sub('[^0-9.]+', '', s)
    return version_apache


# Get current OpenSSH version
def get_version_openssh():
    page = requests.get("https://www.openssh.com/releasenotes.html")
    soup = BeautifulSoup(page.content, 'html.parser')
    release_tags = soup.find_all("h3")
    latest = release_tags[0].findChildren("a", recursive=False)
    s = latest[0].text
    version_ssh = re.sub('[^0-9.]+', '', s)
    return version_ssh

@lru_cache(5)
def get_latest_version(service_id):
    if service_id == APACHE:
        return get_version_apache()
    elif service_id == OPENSSH:
        return get_version_openssh()
    return '???'
