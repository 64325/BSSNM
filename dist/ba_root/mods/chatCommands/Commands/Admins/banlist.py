import os

import ba, _ba

description = 'показать бан-лист'
info = [
    '                              /banlist   [страница]'
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
    show_banlist(client_id, type, page)

def show_banlist(client_id, type, page):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    session.update_banlist()
    ban_list = session.playersData['banlist']
    from chatHandle.chat_functions import translate_time
    ban_list_show = []
    for account_id in ban_list:
        player_line = account_id
        if 'account name' in ban_list[account_id] and ban_list[account_id]['account name'] != account_id:
            player_line += ' | ' + ban_list[account_id]['account name']
        ban_list_show.append(player_line)
        time_line = '       - бан'
        if 'date' in ban_list[account_id]:
            time_line += ' с ' + translate_time(ban_list[account_id]['date'])
        if 'until' in ban_list[account_id]:
            time_line += ' до ' + translate_time(ban_list[account_id]['until'])
        else:
            time_line += ' навсегда'
        ban_list_show.append(time_line)
        if 'reason' in ban_list[account_id]:
            reason_line = '       - причина: ' + ban_list[account_id]['reason']
            ban_list_show.append(reason_line)
    from chatCommands.chat_command_functions import show_pages
    showmessage(client_id, type, '=============== бан-лист: ===============', _white_)
    show_pages(client_id, ban_list_show, type, page)
