from fastapi import FastAPI
from pydantic import BaseModel
import json
from pyautogui import keyDown, keyUp, press, KEYBOARD_KEYS

class Item(BaseModel):
    name: str
    body: str = "{}"

'''
['metaData', 'xcoord', 'ycoord', 'direction', 'target', 'needWater', 'needFood', 'needManaGem', 'playerInCombat', 'targetInCombat', 'targetIsDead', 'health', 'healthCurrent', 'mana', 'manaCurrent', 'range', 'level', 'gold', 'deadStatus', 'talentPoints', 'skinning', 'item', 'equip', 'bags', 'spell', 'gossipWindowOpen', 'itemsAreBroken', 'bagIsFull', 'bindingWindowOpen', 'zone', 'fishing', 'gameTime', 'gossipOptions', 'corpseX', 'corpseY', 'playerClass', 'targetHealth', 'flying', 'hearthZone', 'targetOfTargetIsPlayer', 'bitmask']
'''

def check_target():
    press('7')

def follow_target():
    keyDown('shift')
    press('d')
    keyUp('shift')

def heal_target():
    press('right')
    keyDown('shift')
    press('g')
    keyUp('shift')


def event_loop(state):
    check_target()
    health_perc = int(state['health'])
    if health_perc < 70:
        heal_target()
    else:
        follow_target()

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


