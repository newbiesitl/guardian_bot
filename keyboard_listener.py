import keyboard
import time
max_queue_size = 100
queue = []
keyboard.start_recording(recorded_events_queue=queue)

while True:
    queue = keyboard.stop_recording()
    while len(queue) > 0:
        print(queue[0])
        queue.pop(0)
    keyboard.start_recording(recorded_events_queue=queue)
    time.sleep(1/30)


