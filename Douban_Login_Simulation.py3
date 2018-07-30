#!/usr/bin/python
import requests
header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'}
data={}
S=requests.Session()

response=S.post()

print(response.text)