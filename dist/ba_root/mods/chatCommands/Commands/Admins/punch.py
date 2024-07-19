import math

import ba, _ba

aliases = ['ph']
description = 'изменить силу удара'
info = [
    '                               изменить силу удара',
    '                                    /punch   число'
]

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'введите число', _red_)
        return False
    try:
        value = int(command['args'][0])
        command['args'].pop(0)
    except:
        return False
    value = min(1000000, max(0, value))
    command['parsed_keys']['value'] = math.sqrt(float(value))
    return True

def run_command(client_id, account_id, type, command_keys, player):
    set_punch(player, command_keys['value'])

def set_punch(cl_id, value):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor:
                player.actor._punch_power_scale = 1.2 * value