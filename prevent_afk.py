from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
import random
print(KEYBOARD_KEYS)
keyDown('right')
keyUp('right')
while True:
    try:
        time.sleep(random.randint(10,60))
        keyDown('right')
        keyUp('right')
    except Exception as e:
        print(e)
        keyUp('right')
        time.sleep(1)
        continue
# keyUp('space')
# time.sleep(1)
# keyDown('backspace')
# time.sleep(1)
# keyUp('backspace')



# keyDown('command')
# time.sleep(1)
#
# keyDown('tab')
# time.sleep(0.1)
# keyUp('tab')
# keyUp('command')

