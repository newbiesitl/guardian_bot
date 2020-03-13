import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
url = 'http://127.0.0.1:8000/get_one_sample/'


def get_one_sample(debug=False):
    r = requests.put(url)
    if r.json()['file'] is None:
        return None
    path = r.json()['file']['path']
    seq = r.json()['events']
    # img = Image.open(path)
    with Image.open(path) as img:
        if debug:
            print(np.array(img).shape)
            plt.imshow(img)
            plt.show()
            plt.clf()  # will make the plot window empty
        return np.array(img), seq
