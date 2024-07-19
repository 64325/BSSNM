import math

import ba, _ba

description = 'изменить количество бомб'

using_players_ids = True
timer_compatible = True
info = [
    '                   изменить кол-во бомб у персонажа',
    '                                /bombs   количество'
]

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
    value = min(20, max(0, value))
    command['parsed_keys']['value'] = value
    return True

def run_command(client_id, account_id, type, command_keys, player):
    set_bombs(player, command_keys['value'])

def set_bombs(cl_id, value):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor:
                if value > player.actor._max_bomb_count:
                    player.actor._max_bomb_count = value
                player.actor.bomb_count = value