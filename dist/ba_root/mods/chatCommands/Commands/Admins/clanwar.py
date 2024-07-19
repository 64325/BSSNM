import random

import ba, _ba

aliases = ['kv', 'кв']
description = 'начать клановую войну'
info = [
    'начать клановую войну (нужен режим Elimination)',
    '/kv   team1=игроки   team2=игроки',
    'изменить кол-во очков для победы:',
    '/kv   max=число',
    'изменить названия команд',
    '/kv   name1=название   name2=название',
    "  если в названии несколько слов, берите его в одинарные кавычки  '  '",
    'закончить клановую войну',
    '/kv end'
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
            clanwarmax = int(command['keys']['max'][0])
        except:
            return False
        command['keys'].pop('max')
        command['parsed_keys']['clanwarmax'] = min(30, max(1, clanwarmax))
    if 'name1' in command['keys'] and len(command['keys']['name1']) == 1:
        name1 = command['keys']['name1'][0]
        command['keys'].pop('name1')
        if len(name1) >= 2 and name1[0] == "'" and name1[-1] == "'":
            name1 = name1[1:-1]
        command['parsed_keys']['name1'] = name1
    if 'name2' in command['keys'] and len(command['keys']['name2']) == 1:
        name2 = command['keys']['name2'][0]
        command['keys'].pop('name2')
        if len(name2) >= 2 and name2[0] == "'" and name2[-1] == "'":
            name2 = name2[1:-1]
        command['parsed_keys']['name2'] = name2
    if len(command['args']) == 0 and len(command['keys']) == 0:
        command['parsed_keys']['action'] = 'change'
        return True
    command['parsed_keys']['action'] = 'start'
    if 'vs' in command['args']:
        command['parsed_keys']['team1'] = []
        command['parsed_keys']['team2'] = []
        index = command['args'].index('vs')
        for id_str in command['args'][:index]:
            try:
                id = int(id_str)
                if id in command['parsed_keys']['team1'] or id in command['parsed_keys']['team2']:
                    showmessage(client_id, command['type'], 'номера игроков повторяются', _red_)
                    return False
                command['parsed_keys']['team1'].append(id)
            except:
                return False
        for id_str in command['args'][index+1:]:
            try:
                id = int(id_str)
                if id in command['parsed_keys']['team1'] or id in command['parsed_keys']['team2']:
                    showmessage(client_id, command['type'], 'номера игроков повторяются', _red_)
                    return False
                command['parsed_keys']['team2'].append(id)
            except:
                return False
        command['args'] = []
    elif 'team1' in command['keys'] and 'team2' in command['keys']:
        command['parsed_keys']['team1'] = []
        command['parsed_keys']['team2'] = []
        for id_str in command['keys']['team1']:
            try:
                id = int(id_str)
                if id in command['parsed_keys']['team1'] or id in command['parsed_keys']['team2']:
                    showmessage(client_id, command['type'], 'номера игроков повторяются', _red_)
                    return False
                command['parsed_keys']['team1'].append(id)
            except:
                return False
        command['keys'].pop('team1')
        for id_str in command['keys']['team2']:
            try:
                id = int(id_str)
                if id in command['parsed_keys']['team1'] or id in command['parsed_keys']['team2']:
                    showmessage(client_id, command['type'], 'номера игроков повторяются', _red_)
                    return False
                command['parsed_keys']['team2'].append(id)
            except:
                return False
        command['keys'].pop('team2')
    else:
        showmessage(client_id, command['type'], 'укажите номера игроков', _red_)
        return False
    return True

def run_command(client_id, account_id, type, command_keys):
    if command_keys['action'] == 'end':
        end_clanwar()
        return
    if command_keys['action'] == 'start':
        if 'clanwarmax' in command_keys:
            clanwarmax = command_keys['clanwarmax']
        else:
            clanwarmax = 10
        start_clanwar(client_id, type, command_keys['team1'], command_keys['team2'], clanwarmax)
    if command_keys['action'] == 'change':
        if 'clanwarmax' in command_keys:
            change_clanwar_max(client_id, type, command_keys['clanwarmax'])
    if 'name1' in command_keys:
        change_clanwar_name1(client_id, type, command_keys['name1'])
    if 'name2' in command_keys:
        change_clanwar_name2(client_id, type, command_keys['name2'])

def end_clanwar():
    session = _ba.get_foreground_host_session()
    session.end_clanwar()

def change_clanwar_name1(client_id, type, name1):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    if session.sessionmode != 'clanwar':
        showmessage(client_id, type, 'кв не начато', _red_)
        return
    session.set_clanwar_name_left(name1)

def change_clanwar_name2(client_id, type, name2):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    if session.sessionmode != 'clanwar':
        showmessage(client_id, type, 'кв не начато', _red_)
        return
    session.set_clanwar_name_right(name2)

def change_clanwar_max(client_id, type, clanwarmax):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    if session.sessionmode != 'clanwar':
        showmessage(client_id, type, 'кв не начато', _red_)
        return
    session.set_clanwarscoretowin(clanwarmax)

def start_clanwar(client_id, type, clanwar_ids_left, clanwar_ids_right, clanwarmax):
    from chatHandle.chat_functions import showmessage, _red_
    activity = ba.getactivity()
    session = activity.session
    rost = _ba.get_game_roster()
    rost_ids = [i['client_id'] for i in rost]
    clanwar_accounts_left = []
    clanwar_accounts_right = []
    clanwar_players_left = []
    clanwar_players_right = []
    from ModData.account_info import client_to_display_string
    for id in clanwar_ids_left:
        account_name = client_to_display_string(id)
        if id == -1 or account_name == '':
            showmessage(client_id, type, str(id) + ': игрок не найден', _red_)
            return
        if account_name in clanwar_accounts_left or account_name in clanwar_accounts_right:
            showmessage(client_id, type, account_name + ': игрок повторяется', _red_)
            return
        clanwar_accounts_left.append(account_name)
        player = None
        for player in session.sessionplayers:
            if player.inputdevice.client_id == id and player not in clanwar_players_left and player not in clanwar_players_right:
                clanwar_players_left.append(player)
                break
    for id in clanwar_ids_right:
        account_name = client_to_display_string(id)
        if id == -1 or account_name == '':
            showmessage(client_id, type, str(id) + ': игрок не найден', _red_)
            return
        if account_name in clanwar_accounts_left or account_name in clanwar_accounts_right:
            showmessage(client_id, type, account_name + ': игрок повторяется', _red_)
            return
        clanwar_accounts_right.append(account_name)
        player = None
        for player in session.sessionplayers:
            if player.inputdevice.client_id == id and player not in clanwar_players_left and player not in clanwar_players_right:
                clanwar_players_right.append(player)
                break
    if len(clanwar_players_left) == 0 or len(clanwar_players_right) == 0:
        showmessage(client_id, type, 'в командах не хватает игроков', _red_)
        return
    session.start_clanwar(clanwar_accounts_left, clanwar_accounts_right, clanwar_players_left, clanwar_players_right, clanwarmax)
