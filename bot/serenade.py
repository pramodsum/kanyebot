from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.kanyerest.xyz/serenade"

html = urlopen(section_url).read()
soup = BeautifulSoup(html, "lxml")
print(soup)
