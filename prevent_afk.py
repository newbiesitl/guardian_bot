from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
import random
import pyautogui
pyautogui.FAILSAFE = False
print(KEYBOARD_KEYS)

'''
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']
'''

random.seed(0)

def reload():
    press('enter')
    for char in '/reload':
        press(char)
    press('enter')


movement_options = [
    "left", "right", #"up", "down"
]

def brown_move(up_only=False):
    action_index = random.randint(0,1)
    if not up_only:
        keyDown(movement_options[action_index])
    # time.sleep(0.5)
    keyUp(movement_options[action_index])

def send_message(char_id, msg):
    press('enter')
    msg = '/w %s %s' % (char_id, msg)
    for char in msg:
        press(char)
    press('enter')
reload_counter = 100
counter_reset = 100
time.sleep(5)
# send_message('Warag', 'test started')
brown_move()
while True:
    try:
        time.sleep(30)
        if reload_counter == 0:
            reload_counter = counter_reset
            reload()
        reload_counter -= 1
        keyUp('{')

    except Exception as e:
        print(e)
        keyUp('{')
        time.sleep(1)
        continue
