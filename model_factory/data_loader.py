

import json
LOOK_UP_D_FILE_NAME = 'LD.json'


def dump_dict_to_file(d, file_name):
    json_p = json.dumps(d)
    f = open(file_name, "w+")
    f.write(json_p)
    f.close()

def load_dict(file_name):
    f = open(file_name, 'r')
    json_p = json.load(f)
    return json_p


def unpack_payload(p:[], ld:{}):
    '''
    Payload is a list of two lists
    1 list is list of img array
    1 list is the list of keyboard activities
    they share the same time index
    '''
    imgs = p[0]
    key_seq = p[1]
    idx = 0
    while True:
        if idx >= len(imgs):
            break
        seq = key_seq[idx]
        # tokenize seq
        for t_i in range(len(seq)):
            t = seq[t_i]
            if t in ld:
                seq[t_i] = seq[t]
            else:
                max_idx = len(list(ld.keys()))
                ld[t] = max_idx
                dump_dict_to_file(ld, LOOK_UP_D_FILE_NAME)
        key_seq[idx] = seq
    return (imgs, key_seq)