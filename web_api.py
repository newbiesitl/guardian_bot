from fastapi import FastAPI, File, UploadFile
from collections import OrderedDict
import time, io
import numpy as np
from PIL import Image
app = FastAPI()

event_window_size = 1.0 # 1 sec
event_right_window = -1.0
event_left_window = -1.0

od = OrderedDict()

QUEUE_MAX_LEN = 100
app = FastAPI()

PREV_IMG = None
PREV_TS = -1

@app.post("/uploadfile/")
async def create_upload_file(ts: float, file: bytes = File(...)):
    global PREV_IMG
    global PREV_TS
    global od
    # pop events older than prev_ts
    event_queue = []
    payload = {}

    if PREV_IMG is None:
        image = Image.open(io.BytesIO(file))
        PREV_IMG = image
        payload['image'] = image
        return {'num events': len(event_queue), 'image type': str(type(payload['image']))}
    while True:
        if len(od) == 0:
            payload['image'] = PREV_IMG
            PREV_TS = ts
            image = Image.open(io.BytesIO(file))
            PREV_IMG = image
            break
        first_event = tuple(od.items())[0]
        first_event_time = first_event[0]
        if first_event_time < PREV_TS:
            od.pop(first_event_time)
        elif PREV_TS < first_event_time < PREV_TS + event_window_size:
            event_queue.append(od.pop(first_event_time))
        elif PREV_TS + event_window_size < first_event_time:
            # emit the payload here
            payload['image'] = PREV_IMG
            PREV_TS = ts
            image = Image.open(io.BytesIO(file))
            PREV_IMG = image
            break
    payload['events'] = event_queue
    # return {'image type': type(payload['image']), 'num events': len(event_queue)}
    return {'num events': len(event_queue), 'image type': str(type(payload['image']))}







@app.get("/event/")
async def read_item(name: str, ts: float, event_type: str):
    global event_right_window
    global event_left_window
    global od
    cur_time = time.time()
    if ts < event_left_window:
        return {
            "message": "event outdated",
            "server time": cur_time,
            "event time": ts,
            "event window size": event_window_size,
            'status': "failed"
        }
    event_right_window = ts if ts > event_right_window else event_right_window
    event_left_window = event_right_window - event_window_size
    # add new event to queue
    if ts >= event_right_window:
        od[ts] = {
        "name": name, "ts": ts, "event_type": event_type,
        'status': 'sucess'
    }
    # pop old events
    while len(od.items()) > QUEUE_MAX_LEN:
        first_event = tuple(od.items())[0]
        first_event_time = first_event[0]
        od.pop(first_event_time)

    print('delay %.4f sec' % (cur_time-ts))
    return {
        "num items in queue": len(od.items()),
        "event time": ts,
        "left window": event_left_window,
        "right window": event_right_window,
        'status': 'sucess'
    }