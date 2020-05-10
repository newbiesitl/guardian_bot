from fastapi import FastAPI
from pydantic import BaseModel
import json
from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS
import time
time.sleep(5)
class Item(BaseModel):
    name: str
    body: str = "{}"

'''
['metaData', 'xcoord', 'ycoord', 'direction', 'target', 'needWater', 'needFood', 'needManaGem', 'playerInCombat', 'targetInCombat', 'targetIsDead', 'health', 'healthCurrent', 'mana', 'manaCurrent', 'range', 'level', 'gold', 'deadStatus', 'talentPoints', 'skinning', 'item', 'equip', 'bags', 'spell', 'gossipWindowOpen', 'itemsAreBroken', 'bagIsFull', 'bindingWindowOpen', 'zone', 'fishing', 'gameTime', 'gossipOptions', 'corpseX', 'corpseY', 'playerClass', 'targetHealth', 'flying', 'hearthZone', 'targetOfTargetIsPlayer', 'bitmask']
'''

def check_target():
    press('7')

def follow_target():
    press('3')

def heal_target():
    press('right')
    press('g')

def heal_self():
    press('left')
    press('2')

def mount():
    press('-')

previous_state_in_combat = False

def event_loop(state):
    global previous_state_in_combat
    check_target()
    health = int(state['targetHealth'])
    max_health = int(state['targetHealthMax'])
    if max_health == 0:
        follow_target()
    print('target combat', state['targetInCombat'])
    print('targetHealth  percentage %d/%d' % (state['targetHealth'], state['targetHealthMax']))
    if float(health/max_health) < 0.85:
        heal_target()
    elif float(state['health'])/100 < 0.85:
        heal_self()
    elif not state['targetInCombat'] and previous_state_in_combat:
        mount()
    else:
        follow_target()
    previous_state_in_combat = state['targetInCombat']

app = FastAPI()
menu = None
@app.post("/state/", status_code=200)
async def get_state(item: Item):
    json_body = item.body
    j_load = json.loads(json_body)
    print("""
    player in combat:  %s
    mana: %s, %s%s
    health: %s, %s%s
    target: %s
    """ % (
        j_load['playerInCombat'],
        j_load['manaCurrent'], '%', j_load['mana'],
        j_load['healthCurrent'], '%', j_load['health'],
        j_load['target']
    ))
    global menu
    if menu is None:
        menu = list(j_load.keys())
        print(menu)
    return j_load



@app.post("/action/", status_code=200)
def perform_action(item: Item):
    json_body = item.body
    j_load = json.loads(json_body)
    event_loop(j_load)
    return j_load