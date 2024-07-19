import math

import ba, _ba

description = 'схватить игрока'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите номер игрока', _red_)
        return False
    try:
        value = int(command['args'][0])
        command['args'].pop(0)
    except:
        if command['args'][0] == 'me':
            value = client_id
        else:
            return False
    command['parsed_keys']['player'] = value
    return True

def run_command(client_id, account_id, type, command_keys, player):
    grab(player, command_keys['player'])

def grab(cl_id, target_id):
    activity = ba.getactivity()
    target_player = None
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == target_id:
            if player.actor and player.actor.node:
                target_player = player
    if target_player != None:
        for player in activity.players:
            if player.sessionplayer.inputdevice.client_id == cl_id:
                if player.actor and player.actor.node:
                    player.actor.node.hold_body = 1
                    player.actor.node.hold_node = target_player.actor.node
    