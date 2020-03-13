

import json
LOOK_UP_D_FILE_NAME = 'LD.json'


def dump_dict_to_file(d, file_name):
    json_p = json.dumps(d)
    f = open(file_name, "w+")
    f.write(json_p)
    f.close()

def load_dict(file_name):
    try:
        with open(file_name, 'r') as f:
            json_p = json.load(f)
            return json_p
    except FileNotFoundError:
        tmp = {'null': 0}
        dump_dict_to_file(tmp, file_name)
        return load_dict(file_name)

def tokenize_seq(key_seq:[], ld:{}):
    '''
    key_seq is a list of sequences
    '''
    if ld is None:
        ld = load_dict(LOOK_UP_D_FILE_NAME)
    idx = 0
    ret = []
    # print('outer',key_seq)
    while True:
        if idx >= len(key_seq):
            break
        sub_seq = []
        seq = key_seq[idx]
        # tokenize seq
        for t_i in range(len(seq)):
            key_event = seq[t_i]
            t = '_'.join([key_event['name'], key_event['event_type']])
            if t not in ld:
                max_idx = len(list(ld.keys()))
                # update max_idx
                ld[t] = max_idx
                dump_dict_to_file(ld, LOOK_UP_D_FILE_NAME)
                ld = load_dict(LOOK_UP_D_FILE_NAME)
            sub_seq.append(ld[t])
        ret.append(sub_seq)
        idx += 1
    return ret