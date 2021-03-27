import requests
from bs4 import BeautifulSoup
import re

# Get current Apache version
page = requests.get("https://github.com/apache/httpd/releases")
soup = BeautifulSoup(page.content, 'html.parser')
release_tags = soup.find_all("div", class_="release-timeline-tags release-entry")[0]
items = release_tags.find_all(class_="commit-title")
tonight = items[0].findChildren("a" , recursive=False)[0]
invalid_tags = ['svg', 'path', 'u']
for tag in invalid_tags: 
    for match in tonight.findAll(tag):
        match.replaceWithChildren()
s = str(tonight.contents)
version_apache = re.sub('[^0-9.]+', '', s)
print(version_apache)



# Get current OpenSSH version
page = requests.get("https://www.openssh.com/releasenotes.html")
soup = BeautifulSoup(page.content, 'html.parser')
release_tags = soup.find_all("h3")
latest = release_tags[0].findChildren("a" , recursive=False)
s = latest[0].text
version_ssh = re.sub('[^0-9.]+', '', s)
print(version_ssh)