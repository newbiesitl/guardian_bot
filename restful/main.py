from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np
from pyautogui import press
import time, os, sys
import random
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

on_follow = False
on_standby = False
on_guard = False
assist_commend_received = False
previous_state = None
mounting = False
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


def handle_movement_states(state):
    global previous_state
    global previous_state_in_combat
    global on_follow
    global on_standby
    global on_guard
    global mounting
    if on_standby:
        return
    if on_follow and not mounting:
        follow_captain()
    if on_guard:
        if previous_state != "on_guard":
            cancel_follow()
        else:
            pass
    print(state['mountable'], mounting)
    if state['mountable'] and not state['playerInCombat'] and not mounting:
        mounting = True
        mount()
        time.sleep(3.5)
        mounting = False

def party_idx_to_target(idx):
    if idx == 0:
        press('f1')
    elif idx == 1:
        press('f2')
    elif idx == 2:
        press('f3')
    elif idx == 3:
        press('f4')
    elif idx == 4:
        press('f5')
    else:
        print('invalid party index %d' % (idx))
        pass



assist_spell1_res = False
assist_spell2_res = False
assist_spell3_res = False

def druid_assist_target_seq():
    if assist_commend_received and not (assist_spell1_res or assist_spell2_res or assist_spell3_res):
        pass

def druid_heal_target_seq(health_percentage, conditions):
    action_performed = False
    if conditions[2] == 1:
        if conditions[0] == 0 and health_percentage <= 0.90:
            press('3')
            action_performed = True
        elif conditions[1] == 0 and health_percentage <= 0.6:
            cancel_follow()
            press('2')
            action_performed = True
        elif health_percentage <= 0.80:
            cancel_follow()
            press('4')
            action_performed = True
        else:
            pass
    return action_performed


def lowest_first(state):
    def string_pair_to_perc(n, dn):
        return float(n)/(float(dn))

    heal_conditions = [
        (state['player_RejuvenationActive'],state['player_Regrowth'], 1), # self always within 40 yd
        (state['party1_RejuvenationActive'],state['party1_Regrowth'], state['is_party1_within_40_yard']),
        (state['party2_RejuvenationActive'],state['party2_Regrowth'], state['is_party2_within_40_yard']),
        (state['party3_RejuvenationActive'],state['party3_Regrowth'], state['is_party3_within_40_yard']),
        (state['party4_RejuvenationActive'],state['party4_Regrowth'], state['is_party4_within_40_yard']),
    ]
    party_percentage = [
        float(state['health']) / 100,
        string_pair_to_perc(state['party1_current_health'], state['party1_max_health']) if heal_conditions[1][2] else 1,
        string_pair_to_perc(state['party2_current_health'], state['party2_max_health']) if heal_conditions[2][2] else 1,
        string_pair_to_perc(state['party3_current_health'], state['party3_max_health']) if heal_conditions[3][2] else 1,
        string_pair_to_perc(state['party4_current_health'], state['party4_max_health']) if heal_conditions[4][2] else 1,
        ]
    print(party_percentage)
    lowest_index = np.argmin(party_percentage)
    if party_percentage[lowest_index] >= 1:
        return False
    lowest_conditions = heal_conditions[lowest_index]
    party_idx_to_target(lowest_index)
    return druid_heal_target_seq(party_percentage[lowest_index], lowest_conditions)

def healing_priority_queue(state):
    return lowest_first(state)



def druid_event_loop(state):
    global previous_state_in_combat
    global on_standby
    if on_standby:
        return
    action_performed = healing_priority_queue(state)
    if not action_performed:
        handle_movement_states(state)
    previous_state_in_combat = state['targetInCombat']



@app.post("/action/", status_code=200)
def perform_action(item: Item):
    json_body = item.body
    j_load = json.loads(json_body)
    global on_follow
    global on_standby
    global previous_state
    global on_guard
    global assist_commend_received
    # update global vars to reflect state
    assist_commend_received = True if int(j_load['assist_hook']) == 1 else False
    previous_state = 'follow' if on_follow else ("standby" if on_standby else "guard")
    on_follow = True if int(j_load['follow_hook']) == 1 else False
    on_standby = True if int(j_load['standby_hook']) == 1 else False
    on_guard = True if int(j_load['guard_hook']) == 1 else False
    druid_event_loop(j_load)
    # pally_event_loop(j_load)
    return j_load


def follow_captain():
    press("f2")
    press(",")

def cancel_follow():
    pool = ['left', 'right']
    press(pool[random.randint(0, 1)])


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