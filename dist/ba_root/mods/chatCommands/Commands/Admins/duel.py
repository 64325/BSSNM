import random

import ba, _ba

description = 'начать дуэль'
info = [
    '                                     начать дуэль',
    '                              /duel   игрок1   игрок2',
    '                  изменить кол-во очков для победы',
    '                                 /duel   max=число',
    '                                  закончить дуэль',
    '                                        /duel end'
]

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'end' in command['args']:
        command['args'].remove('end')
        command['parsed_keys']['action'] = 'end'
        if len(command['args']) != 0:
            return False
        return True
    if 'max' in command['keys'] and len(command['keys']['max']) == 1:
        try:
            duelmax = int(command['keys']['max'][0])
        except:
            return False
        command['keys'].pop('max')
        command['parsed_keys']['duelmax'] = min(20, max(1, duelmax))
    if len(command['args']) == 0:
        command['parsed_keys']['action'] = 'change'
        return True
    command['parsed_keys']['action'] = 'start'
    if 'heal' in command['args']:
        command['args'].remove('heal')
        command['parsed_keys']['heal'] = True
    if len(command['args']) < 2:
        showmessage(client_id, command['type'], 'введите номера игроков', _red_)
        return False
    try:
        id_left = int(command['args'][0])
        command['args'].pop(0)
        id_right = int(command['args'][0])
        command['args'].pop(0)
    except:
        return False
    command['parsed_keys']['duel_ids'] = [id_left, id_right]
    return True

def run_command(client_id, account_id, type, command_keys):
    if command_keys['action'] == 'end':
        end_duel()
        return
    if command_keys['action'] == 'change':
        if 'duelmax' in command_keys:
            change_duel_max(client_id, type, command_keys['duelmax'])
            return
    if 'duelmax' in command_keys:
        duelmax = command_keys['duelmax']
    else:
        duelmax = 10
    if 'heal' in command_keys:
        heal = True
    else:
        heal = False
    start_duel(client_id, type, command_keys['duel_ids'], duelmax, heal)

def end_duel():
    session = _ba.get_foreground_host_session()
    session.end_duel()

def change_duel_max(client_id, type, duelmax):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    if session.sessionmode != 'duelmode':
        showmessage(client_id, type, 'дуэль не начата', _red_)
        return
    session.set_duelscoretowin(duelmax)

def start_duel(client_id, type, duel_ids, duelmax, heal):
    from chatHandle.chat_functions import showmessage, _red_
    if duel_ids[0] == duel_ids[1]:
        showmessage(client_id, type, 'игрок один и тот же', _red_)
        return
    activity = ba.getactivity()
    player_left = None
    player_right = None
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == duel_ids[0]:
            player_left = player
        if player.sessionplayer.inputdevice.client_id == duel_ids[1]:
            player_right = player
    if player_left == None:
        showmessage(client_id, type, str(duel_ids[0]) + ': игрок не найден', _red_)
        return
    if player_right == None:
        showmessage(client_id, type, str(duel_ids[1]) + ': игрок не найден', _red_)
        return
    from ModData.account_info import client_to_player
    session = activity.session
    session.start_duel(player_left.sessionplayer, player_right.sessionplayer, duelmax, heal)
