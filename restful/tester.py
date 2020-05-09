import requests
import json

d_body = {
    'key': 'hgiosdjfoiaw;bjoawdg'
}

r = requests.post('http://0.0.0.0/items/', json={
    "body": json.dumps(d_body),
    "name": "test"
})
ret = r.status_code
print(r.json())