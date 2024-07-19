import random

import ba, _ba

description = 'удалить предметы'
info = [
    '                              /clean   номер игрока',
    '                  удалить все предметы:   /clean map'
]

using_players_ids = True
timer_compatible = True


def extract_args(client_id, account_id, command):
    if 'map' in command['args']:
        command['args'].remove('map')
        command['parsed_keys']['action'] = 'clean_map'
        if 'repeat' in command:
            command.pop('repeat')
        if 'is_delayed' in command:
            command.pop('is_delayed')
        return True
    command['parsed_keys']['action'] = 'clean_player'
    return True

def run_command(client_id, account_id, type, command_keys, player):
    clean(client_id, account_id, type, player, command_keys['action'])

def clean(client_id, account_id, type, cl_id, clean_type):
    from chatHandle.chat_functions import showmessage, _light_yellow_
    try:
        activity = ba.getactivity()
        for object in activity.spawned_objects:
            if object != None:
                if clean_type == 'clean_map' or hasattr(object, 'owner_id') and object.owner_id == cl_id:
                    object.handlemessage(ba.DieMessage())
                    object = None
        if clean_type == 'clean_map':
            showmessage(-1, 2, 'карта очищена', _light_yellow_)
    except:
        pass


def show_objects(client_id, type):
    type = 1
    from chatHandle.chat_functions import showmessage, _white_
    showmessage(client_id, type, '=============== предметы: ===============', _white_)
    for object_name in objects:
        showmessage(client_id, type, '    ' + object_name, _white_)