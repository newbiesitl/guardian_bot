from fastapi import FastAPI
from pydantic import BaseModel
import json
from pyautogui import press
import time
import os, sys
cur_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(cur_path, '..')
sys.path.append(root_dir)

from pally import pally_event_loop

time.sleep(5)
class Item(BaseModel):
    name: str
    body: str = "{}"

'''
['metaData', 'xcoord', 'ycoord', 'direction', 'target', 'needWater', 'needFood', 'needManaGem', 'playerInCombat', 'targetInCombat', 'targetIsDead', 'health', 'healthCurrent', 'mana', 'manaCurrent', 'range', 'level', 'gold', 'deadStatus', 'talentPoints', 'skinning', 'item', 'equip', 'bags', 'spell', 'gossipWindowOpen', 'itemsAreBroken', 'bagIsFull', 'bindingWindowOpen', 'zone', 'fishing', 'gameTime', 'gossipOptions', 'corpseX', 'corpseY', 'playerClass', 'targetHealth', 'flying', 'hearthZone', 'targetOfTargetIsPlayer', 'bitmask']
'''


def mount():
    press('-')

previous_state_in_combat = False

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
    is RejuvenationActive: %s
    """ % (
        j_load['playerInCombat'],
        j_load['manaCurrent'], '%', j_load['mana'],
        j_load['healthCurrent'], '%', j_load['health'],
        j_load['target'],
        j_load['RejuvenationActive']
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
    pally_event_loop(j_load)
    return j_load