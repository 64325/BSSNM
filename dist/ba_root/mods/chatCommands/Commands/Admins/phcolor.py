import math

import ba, _ba

description = 'изменить цвет удара'

using_players_ids = True
using_pb_ids = True
info = [
    '                             установить цвет удара',
    '             /phcolor   clr=r,g,b   номер игрока или pb-id',
    '                                удалить цвет удара',
    '                  /phcolor del   номер игрока или pb-id'
]

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'del' in command['args']:
        command['parsed_keys']['action'] = 'delete'
        command['args'].remove('del')
        return True
    command['parsed_keys']['action'] = 'set'
    if len(command['keys']) == 0:
        showmessage(client_id, command['type'], 'укажите цвет', _red_)
        return False
    from ba._activity import actor_colors, get_color
    if 'clr' in command['keys']:
        if len(command['keys']['clr']) == 1:
            color = command['keys']['clr'][0]
            command['keys'].pop('clr')
            if color not in actor_colors:
                showmessage(client_id, command['type'], color + ': цвет не найден', _red_)
                return False
            command['parsed_keys']['color'] = get_color(color)
        elif len(command['keys']['clr']) == 3:
            command['parsed_keys']['color'] = []
            try:
                for i in range(3):
                    value = float(command['keys']['clr'][0])
                    command['keys']['clr'].pop(0)
                    command['parsed_keys']['color'].append(value)
                command['keys'].pop('clr')
            except:
                return False
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    from chatHandle.chat_functions import showmessage, _red_
    if command_keys['action'] == 'delete':
        remove_phcolor(pb_id)
    else:
        set_phcolor(client_id, account_id, type, pb_id, acc_name, command_keys['color'])

def remove_phcolor(pb_id):
    from ModData import effects
    effects.remove_effect(pb_id, 'punchcolor')
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.set_punchcolor()

def set_phcolor(client_id, account_id, type, pb_id, acc_name, color):
    from ModData import effects
    attrs = {
        'color': color
    }
    effects.add_effect(pb_id, acc_name, 'punchcolor', attrs)
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.set_punchcolor()
