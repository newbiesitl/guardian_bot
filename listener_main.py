import time, sys
import pyautogui, keyboard
from multiprocessing import Process
import subprocess, threading
import numpy as np

MAX_FPS = 5


def async_screen_shot():
    start_time = time.time()
    myScreenshot = pyautogui.screenshot().resize((1280, 800))
    np.array(myScreenshot)
    end_time = time.time()
    print('screen shot taking %.3f finish at %.3f time take %.3f' % (start_time, end_time, end_time-start_time) )


def event_loop(e_type='screenshot'):
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
            worker = threading.Thread(target=async_record_event(0.5))
            worker.start()
        else:
            raise ValueError('unknown type %s', e_type)
        worker.join()

def async_record_event(time_window):
    queue = []
    keyboard.start_recording(recorded_events_queue=queue)
    time.sleep(time_window)
    queue = keyboard.stop_recording()
    for event in queue:
        print(event.name, event.event_type, event.time, )


if __name__ == "__main__":
    fps = 2
    app_type = sys.argv[-1]
    event_loop(e_type=app_type)
