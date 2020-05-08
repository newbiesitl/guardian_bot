from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
import random
print(KEYBOARD_KEYS)


random.seed(0)

def reload():
    press('enter')
    for char in '/reload':
        press(char)
    press('enter')


movement_options = [
    "left", "right", #"up", "down"
]

def brown_move():
    action_index = random.randint(0,1)
    keyDown(movement_options[action_index])
    # time.sleep(0.5)
    keyUp(movement_options[action_index])

def send_message(char_id, msg):
    press('enter')
    msg = '/w %s %s' % (char_id, msg)
    for char in msg:
        press(char)
    press('enter')
reload_counter = 20
counter_reset = 30
time.sleep(5)
# send_message('Warag', 'test started')

while True:
    try:
        time.sleep(10)
        if reload_counter == 0:
            reload_counter = counter_reset
            # reload()
        reload_counter -= 1
        brown_move()

    except Exception as e:
        print(e)
        keyUp('right')
        time.sleep(1)
        continue
