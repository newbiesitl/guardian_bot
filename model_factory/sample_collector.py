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


if __name__ == "__main__":
    from model_factory.data_loader import tokenize_seq
    ts = 5
    ts_sample = []
    img_seq = []
    key_seq = []
    while True:
        sample = get_one_sample()
        if sample is None:
            print('none sample returned, repeat request')
            continue
        # print(sample[1])
        img_seq.append(sample[0])
        key_seq.append(sample[1])
        while len(ts_sample) >= ts:
            img_seq.pop(0)
            key_seq.pop(0)
            time.sleep(0.3)
        ret = tokenize_seq(key_seq, None)
        print(type(img_seq[0]))
        print(ret)
        input('enter a key to continue')
        time.sleep(1)
