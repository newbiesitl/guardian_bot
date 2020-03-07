import keyboard
import time
import pyautogui

import numpy as np
def record(record_current=True, screen_shot=True):
    queue = []
    keyboard.start_recording(recorded_events_queue=queue)
    pix = None
    while True:
        time.sleep(1/30)
        queue = keyboard.stop_recording()
        if record_current and screen_shot:
            myScreenshot = pyautogui.screenshot().resize((1280,800))
            # myScreenshot.save('temp.png')
            pix = np.array(myScreenshot)
        if len(queue) > 0:
            first_event = queue[0]
            last_event = queue[-1]
            # screen shot the last key event
            # pix is 4 channels they are r g b a
            # alpha defines the transparency
            print('total events %d, first event %s last event %s' % (len(queue), queue[0], queue[-1]))
            yield (pix, (first_event, last_event))

        while len(queue) > 0:
            queue.pop(0)

        keyboard.start_recording(recorded_events_queue=queue)
        if not record_current and screen_shot:  # record the next 1/30 sec key activity
            myScreenshot = pyautogui.screenshot().resize((1280, 800))
            # myScreenshot.save('temp.png')
            pix = np.array(myScreenshot)




if __name__ == "__main__":
    for event_frame in record(record_current=False, screen_shot=True):
        pix, event = event_frame
        if pix is not None:
            print(pix.shape, event)
        else:
            print(event)