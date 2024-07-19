import random

import ba, _ba

description = 'выдать поверап'
info = [
    '                             выдать игроку поверап',
    '                       /drop   поверап   номер игрока',
    '                           список поверапов: /drop l'
]

using_players_ids = True
timer_compatible = True

subtypes = powerup_types = [
    'ice_bombs',
    'punch',
    'impact_bombs',
    'land_mines',
    'sticky_bombs',
    'triple_bombs',
    'shield',
    'health',
    'curse'
]

def get_powerup_type(powerup_name):
    if 'freeze'.startswith(powerup_name) and powerup_name.startswith('fr') or 'ice_bombs'.startswith(powerup_name) and powerup_name.startswith('ice'):
        powerup_type = 'ice_bombs'
    elif 'punch'.startswith(powerup_name) and powerup_name.startswith('pu'):
        powerup_type = 'punch'
    elif 'impact_bombs'.startswith(powerup_name) and powerup_name.startswith('im'):
        powerup_type = 'impact_bombs'
    elif 'mines'.startswith(powerup_name) and powerup_name.startswith('min') or 'land_mines'.startswith(powerup_name) and powerup_name.startswith('land'):
        powerup_type = 'land_mines'
    elif 'sticky_bombs'.startswith(powerup_name) and powerup_name.startswith('sti'):
        powerup_type = 'sticky_bombs'
    elif 'triple_bombs'.startswith(powerup_name) and powerup_name.startswith('tri'):
        powerup_type = 'triple_bombs'
    elif 'shield'.startswith(powerup_name) and powerup_name.startswith('sh'):
        powerup_type = 'shield'
    elif 'health'.startswith(powerup_name) and powerup_name.startswith('he'):
        powerup_type = 'health'
    elif 'curse'.startswith(powerup_name) and powerup_name.startswith('cu'):
        powerup_type = 'curse'
    else:
        powerup_type = ''
    return powerup_type
    

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'list' in command['args']:
        command['args'].remove('list')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            return False
        return True
    if 'l' in command['args']:
        command['args'].remove('l')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            return False
        return True
    command['parsed_keys']['action'] = 'set'
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите поверап', _red_)
        return False
    powerup_name = command['args'][0]
    command['args'].pop(0)
    powerup_type = get_powerup_type(powerup_name)
    if powerup_type not in powerup_types:
        showmessage(client_id, command['type'], powerup_name + ': поверап не найден', _red_)
        return False
    command['parsed_keys']['powerup_type'] = powerup_type
    command['subtype'] = powerup_type
    return True

def run_command(client_id, account_id, type, command_keys, player):
    from chatHandle.chat_functions import showmessage, _red_
    if command_keys['action'] == 'show':
        show_powerup_types(client_id, type)
        return
    drop_powerup(player, command_keys['powerup_type'])


def drop_powerup(cl_id, powerup_type):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                player.actor.handlemessage(
                    ba.PowerupMessage(powerup_type))

def show_powerup_types(client_id, type):
    type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    showmessage(client_id, type, '=============== поверапы: ===============', _white_)
    for powerup_type in powerup_types:
        showmessage(client_id, type, '    ' + powerup_type, _white_)
