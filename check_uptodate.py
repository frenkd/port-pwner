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
version = re.sub('[^0-9.]+', '', s)

# Get current ssh version

print(version)