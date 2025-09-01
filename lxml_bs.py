"""
#using lxml
from io import BytesIO
from lxml import etree
import requests

url = 'https://nostarch.com'
r = requests.get(url) # GET
content = r.content # bytes

parser = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser = parser) #etree.parse(file object, parser = parser object)
for link in content.findall('//a'): # search including "a"
    print(f"{link.get('href')} -> {link.text}") #link.get(url) => link // link.text => <a> text <a> (description...etc)
"""
=================
"""
#using beautifulsoup
from bs4 import BeautifulSoup as bs
import requests

url = 'http://bing.com'
r = requests.get(url)
tree = bs(r.text, 'html.parser') # tree structure
for link in tree.find_all('a'):
    print(f"{link.get('href')}->{link.text}")
"""