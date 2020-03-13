

import json
LOOK_UP_D_FILE_NAME = 'LD.json'


def dump_dict_to_file(d, file_name):
    json_p = json.dumps(d)
    f = open(file_name, "w+")
    f.write(json_p)
    f.close()

def load_dict(file_name):
    f = open(file_name, 'r+')
    json_p = json.load(f)
    return json_p


def tokenize_seq(key_seq:[], ld:{}):
    '''
    Payload is a list of two lists
    1 list is list of img array
    1 list is the list of keyboard activities
    they share the same time index
    '''
    if ld is None:
        ld = load_dict(LOOK_UP_D_FILE_NAME)
    idx = 0
    ret = []
    # print('outer',key_seq)
    while True:
        if idx >= len(key_seq):
            break
        seq = key_seq[idx]
        # print('inner',seq)
        # tokenize seq
        for t_i in range(len(seq)):
            key_event = seq[t_i]
            # print(key_event)
            t = '_'.join([key_event['name'], key_event['event_type']])
            # print(t)
            if t in ld:
                ret.append(ld[t])
                # seq[t_i] = ld[t]
            else:
                max_idx = len(list(ld.keys()))
                # update max_idx
                ld[t] = max_idx
                dump_dict_to_file(ld, LOOK_UP_D_FILE_NAME)
                ld = load_dict(LOOK_UP_D_FILE_NAME)
        ret.append(seq)
        # key_seq[idx] = seq
        idx += 1
    return ret