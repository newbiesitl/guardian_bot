import keyboard
import time
import pyautogui
import numpy as np

max_queue_size = 100
queue = []
keyboard.start_recording(recorded_events_queue=queue)

while True:
    queue = keyboard.stop_recording()
    if len(queue) > 0:
        last_event = queue[-1]
        myScreenshot = pyautogui.screenshot()
        pix = np.array(myScreenshot)
        # pix is 4 channels they are r g b a
        # alpha defines the transparency
    while len(queue) > 0:
        print(queue[0])
        queue.pop(0)
    keyboard.start_recording(recorded_events_queue=queue)
    time.sleep(1/30)


