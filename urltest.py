"""
#Get request
import urllib.parse
import urllib.request

url = 'https://www.google.com'
with urllib.request.urlopen(url) as response:
    content = response.read()
print(content)
"""
============================================
"""
#POST request
import urllib.parse
import urllib.request

info = {'user':'tim','passwd':'12345'}
url = 'http://boodelyboo.com'
data = urllib.parse.urlencode(info).encode() #urlencode : info(str) encoding, .encode() => str to bytes
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
    content = response.read()
print(content)
"""
============================================
"""
#requsts lib test
import requests
url = 'http://boodelyboo.com'
response = requests.get(url) # GET
data = {'user':'tim', 'passwd':'12345'}
response = requests.post(url, data=data) # POST
print(response.txt) # response.txt => string // response.content => bytestring
"""



