import requests
from PIL import Image
import numpy as np
import time
url = 'http://127.0.0.1:8000/get_one_sample/'


def get_one_sample():
    r = requests.put(url)
    if r.json()['file'] is None:
        return None
    path = r.json()['file']['path']
    img = Image.open(path)
    # print(np.array(img).shape)
    seq = r.json()['events']
    # print(r.json()['events'])
    return np.array(img), seq

