import os

import ba, _ba

description = 'показать список привилегий'
info = [
    '                              /statlist   [страница]'
]

def extract_args(client_id, account_id, command):
    if len(command['args']) != 0:
        try:
            value = int(command['args'][0])
            command['args'].pop(0)
        except:
            return False
        command['parsed_keys']['page'] = max(0, value)
    return True

def run_command(client_id, account_id, type, command_keys):
    if 'page' in command_keys:
        page = command_keys['page']
    else:
        page = 1
    show_statlist(client_id, type, page)

def show_statlist(client_id, type, page):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    session.update_roles()
    roles_list = session.playersData['roles']
    from chatHandle.chat_functions import translate_time
    roles_list_show = []
    for account_id in roles_list:
        player_line = roles_list[account_id]['role']
        player_line += ' | ' + account_id
        if len(roles_list[account_id]['account name']) != 0 and account_id not in roles_list[account_id]['account name']:
            player_line += ' | ' + roles_list[account_id]['account name'][-1]
        roles_list_show.append(player_line)
        time_line = '       - выдана'
        if 'date' in roles_list[account_id]:
            time_line += ' ' + translate_time(roles_list[account_id]['date'])
        if 'until' in roles_list[account_id]:
            time_line += ' до ' + translate_time(roles_list[account_id]['until'])
        else:
            time_line += ' навсегда'
        roles_list_show.append(time_line)
    from chatCommands.chat_command_functions import show_pages
    showmessage(client_id, type, '=============== статус-лист: ===============', _white_)
    show_pages(client_id, roles_list_show, type, page)
