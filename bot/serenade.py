from lxml import html
import requests

page = requests.get('http://www.kanyerest.xyz/serenade')
content = html.fromstring(page.content)

print(content)
