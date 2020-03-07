import keyboard
import time
import pyautogui
import asyncio
import numpy as np

async def async_screen_shot():
    print('screen shot taking', time.time(), )
    myScreenshot = pyautogui.screenshot().resize((1280, 800))
    np.array(myScreenshot)

async def async_record_event(fps):
    queue = []
    keyboard.start_recording(recorded_events_queue=queue)
    await asyncio.sleep(1 / fps)

    # await asyncio.sleep(1/fps)
    queue = keyboard.stop_recording()
    for event in queue:
        print(event.name, event.event_type, event.time, )


async def record(fps=50):
    while True:
        queue = []
        sreen_task = asyncio.create_task(async_screen_shot())
        # keyboard_task = asyncio.create_task(async_record_event(fps))
        keyboard.start_recording(recorded_events_queue=queue)
        await asyncio.sleep(1/fps)
        await sreen_task
        # await keyboard_task
        queue = keyboard.stop_recording()
        for event in queue:
            print(event.name, event.event_type, event.time, )







if __name__ == "__main__":
    asyncio.run(record(fps=5))
