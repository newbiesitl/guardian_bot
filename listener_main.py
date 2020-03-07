import time, sys
import pyautogui, keyboard
import asyncio
from multiprocessing import Process
import requests
import subprocess, threading
import numpy as np

MAX_FPS = 5


def async_screen_shot():
    start_time = time.time()
    myScreenshot = pyautogui.screenshot().resize((1280, 800))
    np.array(myScreenshot)
    end_time = time.time()
    print('screen shot taking %.3f finish at %.3f time take %.3f' % (start_time, end_time, end_time-start_time) )


def event_loop(e_type='screenshot', verbose=False):
    iter = 1
    while True:
        iter += 1
        if iter % 100 == 0:
            subprocess.Popen(['./clean_tmp.sh'], shell=True)
            iter = 0
        if e_type == 'screenshot':
            worker = threading.Thread(target=async_screen_shot())
            worker.start()
        elif e_type == 'keyboard':
            worker = threading.Thread(target=async_record_event(0.5, verbose))
            worker.start()
        else:
            raise ValueError('unknown type %s', e_type)
        worker.join()



async def process_event(queue, verbose=False):
    # keyboard.play(queue)

    for event in queue:
        if verbose:
            print(event.name, event.event_type, event.time, )

        payload = {
            'name': event.name,
            'ts': event.time,
            'event_type': event.event_type,
        }
        r = requests.get('http://127.0.0.1:8000/event', params=payload)
        print(r.json())

def async_record_event(time_window, verbose=False):
    queue = []
    keyboard.start_recording(recorded_events_queue=queue)
    time.sleep(time_window)
    queue = keyboard.stop_recording()
    asyncio.run(process_event(queue, verbose))

if __name__ == "__main__":
    fps = 2
    app_type = sys.argv[-1]
    event_loop(e_type=app_type, verbose=False)
