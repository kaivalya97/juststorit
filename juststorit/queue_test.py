import json
import requests.exceptions
from flask import Flask, request

url = "http://10.20.24.90:5001/queue"
url2 = "http://10.20.24.90:5001/queuepop"

headers = {'Content-Type': 'application/json'}
r = requests.post(
    url,
    data=json.dumps({
        'uid': 1000,
        'filename': "A",
        'op': 1
    }),
    headers=headers)
print r.text

r = requests.post(
    url,
    data=json.dumps({
        'uid': 1001,
        'filename': "B",
        'op': 2
    }),
    headers=headers)
print r.text

req = requests.get(url2, headers=headers)
print req.text
