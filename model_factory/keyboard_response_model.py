from model_arch.multi_channel import get_seq_model
import time
from model_factory.sample_collector import get_one_sample
import numpy as np
from keras.preprocessing.sequence import pad_sequences

# https://github.com/dmlc/xgboost/issues/1715
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

multifier = 2 # down and up

reserved_keyspace = 128 * multifier

num_keys = reserved_keyspace
seq_len = 20
h_dim = 10
frames = 3
model = get_seq_model(num_keys = num_keys,
                    seq_len = seq_len,
                    h_dim = h_dim,
                    frames = frames,)
model.summary()

from model_factory.data_loader import tokenize_seq

ts = frames
ts_sample = []
img_seq = []
key_seq = []
while True:
    sample = get_one_sample(debug=False)
    if sample is None:
        # print('none sample returned, repeat request')
        continue
    # print(sample[1])
    img_seq.append(sample[0])
    key_seq.append(sample[1])
    ret = tokenize_seq(key_seq, None)
    # last frame is label
    while len(img_seq) > ts + 1:
        # all data preprocessing are here!
        img_seq.pop(0)
        ret.pop(0)
        label_seq = ret[-1:]
        input_img_seq = img_seq[:-1]
        input_key_seq = ret[:-1]
        label_seq = np.array(label_seq)
        input_img_seq = np.array(input_img_seq)
        input_key_seq = np.array(input_key_seq)
        print(label_seq)
        input_key_seq = pad_sequences(input_key_seq,seq_len,value=0,dtype='int32')
        label_seq = pad_sequences(label_seq,seq_len,value=0,dtype='int32')
        label_seq = np.expand_dims(label_seq, -1)
        print(input_key_seq.shape)
        print(label_seq.shape)
        model.fit([[input_img_seq], [input_key_seq]], [label_seq], batch_size=1)
    # print(type(img_seq[0]))
    time.sleep(.1)