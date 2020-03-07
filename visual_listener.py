import keyboard
import time
import pyautogui
import asyncio
import numpy as np

async def async_screen_shot():
    print('screen shot', time.time(), )
    myScreenshot = pyautogui.screenshot().resize((1280, 800))
    np.array(myScreenshot)

async def async_record_event(fps):
    queue = []
    keyboard.start_recording(recorded_events_queue=queue)
    await asyncio.sleep(1/fps)
    queue = keyboard.stop_recording()
    for event in queue:
        print(event.name, event.event_type, event.time, )


def record(fps=50):
    while True:
        # asyncio.run(async_record_event(fps))
        queue = []
        keyboard.start_recording(recorded_events_queue=queue)
        asyncio.run(async_screen_shot())
        # time.sleep(1/fps)
        queue = keyboard.stop_recording()
        for event in queue:
            print(event.name, event.event_type, event.time, )
        # await asyncio.sleep(1/fps)








if __name__ == "__main__":
    record(fps=20)
