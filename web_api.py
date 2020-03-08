from fastapi import FastAPI, File, UploadFile
from collections import OrderedDict
import time, io
import numpy as np
from PIL import Image
app = FastAPI()

event_window_size = 1 # 1 sec
event_right_window = -1
event_left_window = -1

od = OrderedDict()


app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: bytes = File(...)):
    image = Image.open(io.BytesIO(file))
    return {"image_shape": np.array(image).shape}







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
    # pop old events
    while len(od.items()) > 0:
        first_event = tuple(od.items())[0]
        first_event_time = first_event[0]
        if first_event_time < event_left_window:
            od.pop(first_event_time)
        else:
            break
    # add new event to queue
    if ts >= event_right_window:
        od[ts] = {
        "name": name, "ts": ts, "event_type": event_type,
        'status': 'sucess'
    }

    print('delay %.4f sec' % (cur_time-ts))
    return {
        "num items in queue": len(od.items()),
        "event time": ts,
        "left window": event_left_window,
        "right window": event_right_window,
        'status': 'sucess'
    }