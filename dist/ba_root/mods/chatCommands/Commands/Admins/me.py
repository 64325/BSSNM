import os

import ba, _ba

aliases = ['stats']
description = 'показать статистику'
info = [
    '                         увидеть информацию о игроке',
    '                    /me   номер игрока, pb-id или аккаунт'
]

using_players_ids = True
using_pb_ids = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    from chatHandle.chat_functions import string_type
    session = _ba.get_foreground_host_session()
    for arg in command['args']:
        if (string_type(arg) == 'name' or string_type(arg) == 'notype') and arg != 'a' and arg != 'all' and arg != 'me' and not arg.startswith('-'):
            acc_id = ''
            for account_id in session.playersData['stats']:
                if 'account name' in session.playersData['stats'][account_id]:
                    for account_name in session.playersData['stats'][account_id]['account name']:
                        if account_name != '' and (account_name[1:] == arg or account_name == arg):
                            command['args'].append(account_id)
                            acc_id = account_id
                            break
            if acc_id == '':
                showmessage(-1, 1, arg + ': игрок не найден', _red_)
            command['args'].remove(arg)
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    show_me_info(client_id, type, pb_id, acc_name)

def show_me_info(client_id, type, pb_id, acc_name):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    from ModData.account_info import client_to_account, client_to_display_string
    rost = _ba.get_game_roster()
    cl_id = -1
    for i in rost:
        if i['account_id'] == pb_id:
            cl_id = i['client_id']
            acc_name = i['display_string']
    session = _ba.get_foreground_host_session()
    from ModData import me
    me_info, me_names = me.get_me_info(cl_id, pb_id, acc_name)
    me_text = []
    me_text.append('____________________ Info ____________________')
    accounts_line = ''
    acc_names = me_info['account_names']
    if len(acc_names) > 4:
        acc_names = acc_names[:4] + [' ...']
    for acc in acc_names:
        if acc != '':
            if accounts_line != '':
                accounts_line += '  ·  '
            accounts_line += acc
    if accounts_line != '':
        me_text.append(accounts_line)
    account_info_line = '  ' + ('   ' if cl_id == -1 else str(cl_id)) + '     ·     ' + (' ? ' if pb_id == '' else pb_id) + '                   ' + '<  ' + me_info['role'] + '  >'
    me_text.append(account_info_line)
    me_text.append('                  __________________________          ')
    if accounts_line != '':
        me_names_line = ''
        me_values_line = ''
        for key in me_info:
            name = me_names[key]
            value = me_info[key]
            if key not in ['client_id', 'account_id', 'account_name', 'account_names', 'role']:
                if me_names_line != '':
                    me_names_line += '    '
                    me_values_line += '    '
                e1 = int(max(1, (len(name) - len(value)) / 2))
                e2 = int(max(1, (len(name) - len(value) + 1) / 2))
                value = '  ' * e1 + value + '  ' * e2
                if len(name) < 6:
                    me_names_line += '  ' * (6 - len(name))
                    me_values_line += '  ' * (6 - len(name))
                me_names_line += name
                me_values_line += value
                if len(name) < 6:
                    me_names_line += '  ' * (6 - len(name))
                    me_values_line += '  ' * (6 - len(name))
        me_text.append(me_names_line)
        me_text.append(me_values_line)
            

    for line in me_text:
        showmessage(client_id, type, line, _white_)
