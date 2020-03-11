import requests
from PIL import Image
import numpy as np
url = 'http://127.0.0.1:8000/get_one_sample/'

with requests.put(url) as r:
    # r = requests.put(url)
    path = r.json()['file']['path']
    print(r.json()['file'])
    try:
        img  = Image.open(path)
        print(np.array(img).shape)
    except IOError as e:
        print(e)
        pass
    print(r.json()['events'])