import random

import ba, _ba

aliases = ['par']
description = 'добавить партиклы'
info = [
    '                              добавить партиклы',
    '/particles   тип   [t=интервал]   [size=размер]   номер игрока или pb-id',
    '                               удалить партиклы',
    '                /particles del   номер игрока или pb-id',
    '                               список партиклов',
    '                                    /particles list'
]

using_players_ids = True
using_pb_ids = True

subtypes = particle_types = [
    'ice',
    'snow',
    'slime',
    'spark',
    'metal',
    'rock',
    'splinter',
    'sweat',
    'smoke',
    'steam',
    'devil',
    'fairy',
    'snowcloud',
    'raincloud'
]

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'del' in command['args']:
        command['args'].remove('del')
        command['parsed_keys']['action'] = 'delete'
        return True
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
    if 'size' in command['keys'] and len(command['keys']['size']) == 1:
        try:
            command['parsed_keys']['size'] = float(command['keys']['size'][0])
            command['keys'].pop('size')
        except:
            return False
    if 't' in command['keys'] and len(command['keys']['t']) == 1:
        try:
            command['parsed_keys']['time_interval'] = float(command['keys']['t'][0])
            command['keys'].pop('t')
        except:
            return False
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите тип партиклов', _red_)
        return False
    particle_type = command['args'][0]
    command['args'].pop(0)
    if particle_type not in particle_types:
        showmessage(client_id, command['type'], particle_type + ': тип не найден', _red_)
        return False
    command['parsed_keys']['particle_type'] = particle_type
    command['subtype'] = particle_type
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    from chatHandle.chat_functions import showmessage, _red_
    if command_keys['action'] == 'delete':
        remove_particles(pb_id)
    elif command_keys['action'] == 'show':
        show_particle_types(client_id, type)
    else:
        session = ba.getactivity().session
        if 'size' in command_keys:
            size = min(5.0, max(0.1, command_keys['size']))
        else:
            size = 1.0
        if 'time_interval' in command_keys:
            time_interval = min(1000.0, max(0.02, command_keys['time_interval']))
        else:
            time_interval = 0.5
        set_particles(client_id, account_id, type, pb_id, acc_name, command_keys['particle_type'], size, time_interval)

def remove_particles(pb_id):
    from ModData import effects
    effects.remove_effect(pb_id, 'particles')
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.remove_particles()

def set_particles(client_id, account_id, type, pb_id, acc_name, particle_type, size, time_interval):
    from ModData import effects
    attrs = {
        'type': particle_type,
        'size': size,
        'time_interval': time_interval
    }
    effects.add_effect(pb_id, acc_name, 'particles', attrs)
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.set_particles()

def show_particle_types(client_id, type):
    type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    showmessage(client_id, type, '=============== партиклы: ===============', _white_)
    for particle_type in particle_types:
        showmessage(client_id, type, '    ' + particle_type, _white_)
