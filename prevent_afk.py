from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
import random
print(KEYBOARD_KEYS)
keyDown('right')
keyUp('right')
def reload():
    press('enter')
    for char in '/reload':
        press(char)
    press('enter')
reload_counter = 20
counter_reset = 20
while True:
    try:
        time.sleep(10)
        if reload_counter == 0:
            reload_counter = counter_reset
            reload()
        reload_counter -= 1
        # keyDown('right')
        # keyUp('right')
    except Exception as e:
        print(e)
        keyUp('right')
        time.sleep(1)
        continue
