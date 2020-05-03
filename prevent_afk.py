from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
print(KEYBOARD_KEYS)
while True:
    try:
        time.sleep(5)
        keyDown('right')
        keyUp('right')
        time.sleep(20)
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

