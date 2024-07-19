import os

import ba, _ba

aliases = ['top']
description = 'показать топ'

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
    show_toplist(client_id, type, page)

def show_toplist(client_id, type, page):
    type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    from ModData.ranking import get_rank, get_top_list
    toplist = get_top_list(20)
    toplist_show = []
    for account_id in toplist:
        player_line = '#' + str(get_rank(account_id)) + '  ' + account_id
        if len(session.playersData['stats'][account_id]['account name']) != 0:
            player_line += '  |  ' + session.playersData['stats'][account_id]['account name'][-1]
        if session.playersData['stats'][account_id]['last player name'] != '':
            player_line += '  |  ' + session.playersData['stats'][account_id]['last player name']
        toplist_show.append(player_line)
    from chatCommands.chat_command_functions import show_pages
    showmessage(client_id, type, '=============== топ-лист: ===============', _white_)
    show_pages(client_id, toplist_show, type, 1, long = True)
