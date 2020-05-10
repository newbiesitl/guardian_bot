from pyautogui import press

from restful.main import mount


def pally_event_loop(state):
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