import os

import ba, _ba

description = 'показать мут-лист'
info = [
    '                              /mutelist   [страница]'
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
    show_mutelist(client_id, type, page)

def show_mutelist(client_id, type, page):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    session.update_mutelist()
    mute_list = session.playersData['mutelist']
    from chatHandle.chat_functions import translate_time
    mute_list_show = []
    for account_id in mute_list:
        player_line = account_id
        if 'account name' in mute_list[account_id] and mute_list[account_id]['account name'] != account_id:
            player_line += ' | ' + mute_list[account_id]['account name']
        mute_list_show.append(player_line)
        time_line = '       - мут'
        if 'date' in mute_list[account_id]:
            time_line += ' с ' + translate_time(mute_list[account_id]['date'])
        if 'until' in mute_list[account_id]:
            time_line += ' до ' + translate_time(mute_list[account_id]['until'])
        else:
            time_line += ' навсегда'
        mute_list_show.append(time_line)
        if 'reason' in mute_list[account_id]:
            reason_line = '       - причина: ' + mute_list[account_id]['reason']
            mute_list_show.append(reason_line)
    from chatCommands.chat_command_functions import show_pages
    showmessage(client_id, type, '=============== мут-лист: ===============', _white_)
    show_pages(client_id, mute_list_show, type, page)
