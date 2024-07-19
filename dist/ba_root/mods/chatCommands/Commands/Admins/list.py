import os

import ba, _ba

aliases = ['l']
description = 'показать список игроков'

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    show_list(client_id, type)

def show_list(client_id, type):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    rost = _ba.get_game_roster()
    session = _ba.get_foreground_host_session()
    showmessage(client_id, type, '============= список игроков: =============', _white_)
    if session.sessionmode == 'duelmode':
        duelplayers = []
        for player in session.duelplayers:
            duelplayers.append(player.inputdevice.client_id)
    elif session.sessionmode == 'clanwar':
        clanwarteams = [[], []]
        for player in session.clanwar_teams[0]:
            clanwarteams[0].append(player.inputdevice.client_id)
        for player in session.clanwar_teams[1]:
            clanwarteams[1].append(player.inputdevice.client_id)
    for i in rost:
        if i['client_id'] != -1:
            client_str = ''
            client_str += str(i['client_id'])
            client_str += ' | '
            client_str += i['account_id']
            client_str += ' | '
            client_str += i['display_string']
            if len(i['players']) != 0:
                client_str += ' | '
                client_str += i['players'][0]['name']
            if (session.sessionmode != 'duelmode' or not i['client_id'] in duelplayers) and (session.sessionmode != 'clanwar' or not i['client_id'] in clanwarteams[0] and not i['client_id'] in clanwarteams[1]):
                showmessage(client_id, type, client_str, _white_)
    if session.sessionmode == 'duelmode':
        showmessage(client_id, type, ' ', _white_)
        showmessage(client_id, type, '                                дуэль:', _white_)
        for i in rost:
            if i['client_id'] != -1:
                client_str = ''
                client_str += str(i['client_id'])
                client_str += ' | '
                client_str += i['account_id']
                client_str += ' | '
                client_str += i['display_string']
                if len(i['players']) != 0:
                    client_str += ' | '
                    client_str += i['players'][0]['name']
                    if i['client_id'] in duelplayers:
                        showmessage(client_id, type, client_str, _white_)
    elif session.sessionmode == 'clanwar':
        showmessage(client_id, type, ' ', _white_)
        showmessage(client_id, type, '                                кв:', _white_)
        showmessage(client_id, type, '                   ' + session.clanwar_names[0], _white_)
        for i in rost:
            if i['client_id'] != -1:
                client_str = ''
                client_str += str(i['client_id'])
                client_str += ' | '
                client_str += i['account_id']
                client_str += ' | '
                client_str += i['display_string']
                if len(i['players']) != 0:
                    client_str += ' | '
                    client_str += i['players'][0]['name']
                    if i['client_id'] in clanwarteams[0]:
                        showmessage(client_id, type, client_str, _white_)
        showmessage(client_id, type, '                   ' + session.clanwar_names[1], _white_)
        for i in rost:
            if i['client_id'] != -1:
                client_str = ''
                client_str += str(i['client_id'])
                client_str += ' | '
                client_str += i['account_id']
                client_str += ' | '
                client_str += i['display_string']
                if len(i['players']) != 0:
                    client_str += ' | '
                    client_str += i['players'][0]['name']
                    if i['client_id'] in clanwarteams[1]:
                        showmessage(client_id, type, client_str, _white_)
