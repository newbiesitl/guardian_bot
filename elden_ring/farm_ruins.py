from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
this_key = 'g'
def press_key(this_key):
    keyDown(this_key)
    time.sleep(0.5)
    keyUp(this_key)

time.sleep(5)

while True:
    time.sleep(5)
    press_key('g')


