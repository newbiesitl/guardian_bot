import requests

url = 'http://127.0.0.1:8000/get_one_sample/'

r = requests.put(url)
print(r.json()['file'])
print(r.json()['events'])