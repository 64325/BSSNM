import random
import math

import ba, _ba

description = 'изменить скин'
info = [
    '                                  установить скин',
    '            /skin    имя скина   номер игрока или pb-id',
    '                     скин до выхода с сервера: lobby',
    '                               скин навсегда: global'
]

using_players_ids = True
timer_compatible = True

subtypes = skin_names = {
    'santa': 'Santa Claus',
    'frosty': 'Frosty',
    'bones': 'Bones',
    'bear': 'Bernard',
    'pixel': 'Pixel',
    'penguin': 'Pascal',
    'taobao': 'Taobao Mascot',
    'agent': 'Agent Johnson',
    'wizard': 'Grumbledorf',
    'b9000': 'B-9000',
    'bunny': 'Easter Bunny',
    'kronk': 'Kronk',
    'zoe': 'Zoe',
    'mel': 'Mel',
    'ninja': 'Snake Shadow',
    'pirate': 'Jack Morgan',
    'spaz': 'Spaz',
    'random': 'Spaz'
}

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'del' in command['args'] or 'lobby' in command['args'] or 'global' in command['args'] or 'list' in command['args'] or 'l' in command['args']:
        if 'repeat' in command:
            command.pop('repeat')
        if 'is_delayed' in command:
            command.pop('is_delayed')
    if 'del' in command['args']:
        command['args'].remove('del')
        command['parsed_keys']['action'] = 'delete'
        return True
    if 'list' in command['args']:
        command['args'].remove('list')
        command['parsed_keys']['action'] = 'show'
        return True
    if 'l' in command['args']:
        command['args'].remove('l')
        command['parsed_keys']['action'] = 'show'
        return True
    command['parsed_keys']['action'] = 'set'
    if 'lobby' in command['args']:
        command['args'].remove('lobby')
        command['parsed_keys']['type'] = 'lobby'
    elif 'global' in command['args']:
        command['args'].remove('global')
        command['parsed_keys']['type'] = 'global'
    else:
        command['parsed_keys']['type'] = 'local'
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите название скина', _red_)
        return False
    skin_name = command['args'][0]
    command['args'].pop(0)
    if skin_name not in skin_names:
        showmessage(client_id, command['type'], skin_name + ': скин не найден', _red_)
        return False
    command['parsed_keys']['skin_name'] = skin_name
    command['subtype'] = skin_name
    return True

def run_command(client_id, account_id, type, command_keys, player):
    if command_keys['action'] == 'delete':
        delete_and_remove_skin(client_id, account_id, type, player)
    elif command_keys['action'] == 'show':
        show_skin_names(client_id, type)
    else:
        delete_and_set_skin(client_id, account_id, type, player, command_keys['skin_name'], command_keys['type'])

def run_command_timer_on(client_id, account_id, type, command_keys, player):
    if command_keys['action'] == 'delete':
        remove_skin(client_id, account_id, type, player)
    elif command_keys['action'] == 'show':
        return
    else:
        set_skin(client_id, account_id, type, player, command_keys['skin_name'], command_keys['type'])

def remove_skin(client_id, account_id, type, cl_id):
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            player.character = player.sessionplayer.character
            if player.actor and player.actor.node:
                set_character(player.actor, player.sessionplayer.character)

def delete_and_remove_skin(client_id, account_id, type, cl_id):
    from ModData.account_info import client_to_account
    pb_id = client_to_account(cl_id)
    from ModData import effects
    effects.remove_effect(pb_id, 'skin')
    activity = ba.getactivity()
    activity.session.update_effects()
    if pb_id in activity.session.localPlayersData['effects'] and 'skin' in activity.session.localPlayersData['effects'][pb_id]:
        activity.session.localPlayersData['effects'][pb_id].pop('skin')
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                pos = player.actor.node.torso_position
                try:
                    angle = math.atan2((player.actor.node.position_forward[2] - player.actor.node.position[2]), -(player.actor.node.position_forward[0] - player.actor.node.position[0]))
                except:
                    angle = 0
                angle = 360.0 / 2.0 / math.pi * angle
                player.actor.handlemessage(ba.DieMessage(immediate=True))
                player.character = player.sessionplayer.character
                activity.spawn_player_spaz(player)
                player.actor.node.handlemessage('stand', pos[0], pos[1] - 1.0, pos[2], 90.0 + angle)

def set_skin(client_id, account_id, type, cl_id, skin_name, skin_type):
    if skin_name == 'random':
        skin_name = random.choice(list(skin_names))
    from ModData import effects
    from chatHandle.chat_functions import showmessage, _red_
    activity = ba.getactivity()
    from ModData.account_info import client_to_account
    pb_id = client_to_account(cl_id)
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                set_character(player.actor, skin_names[skin_name])

def delete_and_set_skin(client_id, account_id, type, cl_id, skin_name, skin_type):
    if skin_name == 'random':
        skin_name = random.choice(list(skin_names))
    from ModData import effects
    from chatHandle.chat_functions import showmessage, _red_
    activity = ba.getactivity()
    from ModData.account_info import client_to_account
    pb_id = client_to_account(cl_id)
    if skin_type == 'lobby' or skin_type == 'global':
        if pb_id not in activity.session.localPlayersData['effects']:
            activity.session.localPlayersData['effects'][pb_id] = {}
        activity.session.localPlayersData['effects'][pb_id]['skin'] = skin_names[skin_name]
    if skin_type == 'global':
        if pb_id in activity.session.playersData['stats'] and len(activity.session.playersData['stats'][pb_id]['account name']) != 0:
            acc_name = activity.session.playersData['stats'][pb_id]['account name'][-1]
        else:
            acc_name = ''
        effects.add_effect(pb_id, acc_name, 'skin', skin_names[skin_name])
    activity.session.update_effects()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                pos = player.actor.node.torso_position
                try:
                    angle = math.atan2((player.actor.node.position_forward[2] - player.actor.node.position[2]), -(player.actor.node.position_forward[0] - player.actor.node.position[0]))
                except:
                    angle = 0
                angle = 360.0 / 2.0 / math.pi * angle
                player.actor.handlemessage(ba.DieMessage(immediate=True))
                prev_char, player.character = player.character, skin_names[skin_name]
                activity.spawn_player_spaz(player)
                if skin_type == 'local':
                    player.character = prev_char
                player.actor.node.handlemessage('stand', pos[0], pos[1] - 1.0, pos[2], 90.0 + angle)

def set_character(actor, character):
        from bastd.actor.spazfactory import SpazFactory
        actor.invisible = False
        factory = SpazFactory.get()
        media = factory.get_media(character)
        for attr in media:
            setattr(actor.node, attr, media[attr])


def show_skin_names(client_id, type):
    type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    showmessage(client_id, type, '=============== скины: ===============', _white_)
    for skin_name in skin_names:
        showmessage(client_id, type, '    ' + skin_name, _white_)
