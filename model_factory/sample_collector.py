import requests
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt
ip_addr = 'http://192.168.1.140'
# ip_addr = 'http://127.0.0.1:8000'
img_url = '%s/get_one_sample/' % (ip_addr)
seq_url = '%s/get_one_event_seq/' % (ip_addr)
pop_url = '%s/pop_queue/' % (ip_addr)


def get_one_sample(debug=False):
    # r = requests.put(url)
    with requests.put(img_url) as r:
        seq_r = requests.put(seq_url)
        seq = seq_r.json()['events']
        imageStream = io.BytesIO(r.content)
        with Image.open(imageStream) as img:
            if debug:
                print(np.array(img).shape)
                plt.imshow(img)
                plt.show()
                plt.clf()  # will make the plot window empty
            requests.put(pop_url)
            return np.array(img), seq



if __name__ == "__main__":
    import time
    sample = get_one_sample(debug=True)

    # while True:
    #     sample = get_one_sample(debug=True)
    #     time.sleep(1)