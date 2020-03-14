import time, sys
import pyautogui, keyboard, io
import asyncio
import requests
import subprocess, threading



MAX_FPS = 5
ip_addr = 'http://192.168.1.140'
# ip_addr = 'http://127.0.0.1:8000'
image_upload_url = '%s/uploadfile' % (ip_addr)
event_url = '%s/event' % (ip_addr)

def async_screen_shot():
    try:
        start_time = time.time()
        myScreenshot = pyautogui.screenshot().convert('RGB').resize((640, 480))
        imgByteArr = io.BytesIO()
        myScreenshot.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        # print(type(imgByteArr))
        files = {'file': imgByteArr}
        params = {'ts': start_time}
        r = requests.post(image_upload_url, files=files, params=params)
        print(r.json())
        end_time = time.time()
        print('screen shot taking %.3f finish at %.3f time take %.3f' % (start_time, end_time, end_time - start_time))
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except Exception as e:
        print(e)



def event_loop(fps=30, e_type='screenshot', verbose=False):
    iter = 1
    while True:
        if e_type == 'screenshot':
            worker = threading.Thread(target=async_screen_shot())
            worker.start()
            iter += 1
            if iter % 10 == 0:
                sub_p = subprocess.Popen(['./clean_tmp.sh'], shell=True)
                iter = 0
                sub_p.wait()
        elif e_type == 'keyboard':
            worker = threading.Thread(target=keyboard_listener(1 / fps, verbose))
            worker.start()
        else:
            raise ValueError('unknown type %s', e_type)
        # worker.join()



async def process_event(queue, verbose=False):
    for event in queue:
        if verbose:
            print(event.name, event.event_type, event.time, )

        payload = {
            'name': event.name,
            'ts': event.time,
            'event_type': event.event_type,
        }
        try:
            r = requests.get(event_url, params=payload)
            print('num items in queue %d' % r.json()['num items in queue'])
        except:
            print('exception sending event', payload)


def keyboard_listener(time_window, verbose=False):
    queue = []
    keyboard.start_recording(recorded_events_queue=queue)
    time.sleep(time_window)
    queue = keyboard.stop_recording()
    asyncio.run(process_event(queue, verbose))

if __name__ == "__main__":
    fps = 10
    app_type = sys.argv[-1]
    event_loop(fps=fps, e_type=app_type, verbose=False)
