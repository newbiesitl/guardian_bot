from fastapi import FastAPI
from pydantic import BaseModel
import json
from pyautogui import press
import time
import os, sys
cur_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(cur_path, '..')
sys.path.append(root_dir)

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
    party1 health: %d/%d
    party1 RejuvenationActive %s RegrowthActive %s within 40 yard %s
    party2 health: %d/%d 
    party2 RejuvenationActive %s RegrowthActive %s within 40 yard %s
    party3 health: %d/%d
    party3 RejuvenationActive %s RegrowthActive %s within 40 yard %s
    party4 health: %d/%d
    party4 RejuvenationActive %s RegrowthActive %s within 40 yard %s
    follow: %s
    stand by: %d
    """ % (
        j_load['playerInCombat'],
        j_load['manaCurrent'], '%', j_load['mana'],
        j_load['healthCurrent'], '%', j_load['health'],
        j_load['target'],
        float(j_load['party1_current_health']),float(j_load['party1_max_health']),
        j_load['party1_RejuvenationActive'],j_load['party1_Regrowth'], j_load['is_party1_within_40_yard'],
        float(j_load['party2_current_health']),float(j_load['party2_max_health']),
        j_load['party2_RejuvenationActive'],j_load['party2_Regrowth'], j_load['is_party2_within_40_yard'],
        float(j_load['party3_current_health']),float(j_load['party3_max_health']),
        j_load['party3_RejuvenationActive'],j_load['party3_Regrowth'], j_load['is_party3_within_40_yard'],
        float(j_load['party4_current_health']),float(j_load['party4_max_health']),
        j_load['party4_RejuvenationActive'],j_load['party4_Regrowth'], j_load['is_party4_within_40_yard'],
        j_load['follow_hook'],
        j_load['standby_hook'],
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
    # pally_event_loop(j_load)
    return j_load


def pally_event_loop(state):
    global previous_state_in_combat
    check_target()
    health = int(state['targetHealth'])
    max_health = int(state['targetHealthMax'])
    if max_health <= 0:
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
        press('7') # cleanse self
        follow_target()
        cleanse()
    previous_state_in_combat = state['targetInCombat']


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


def cleanse():
    press('y')