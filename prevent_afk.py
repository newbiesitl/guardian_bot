from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
import random
print(KEYBOARD_KEYS)

def reload():
    press('enter')
    for char in '/reload':
        press(char)
    press('enter')


def send_message(char_id, msg):
    press('enter')
    msg = '/w %s %s' % (char_id, msg)
    for char in msg:
        press(char)
    press('enter')
reload_counter = 20
counter_reset = 30
time.sleep(5)
send_message('Warag', 'test started')
while True:
    try:
        time.sleep(30)
        if reload_counter == 0:
            reload_counter = counter_reset
            # reload()
        reload_counter -= 1
        press('right')
        press('left')

    except Exception as e:
        print(e)
        keyUp('right')
        time.sleep(1)
        continue
