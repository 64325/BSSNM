import os

import ba, _ba

description = 'показать варн-лист'
info = [
    '                           список предупреждений',
    '                             /warnlist   [страница]'
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
    session.update_warnlist()
    warn_list = session.playersData['warnlist']
    from chatHandle.chat_functions import translate_time
    warn_list_show = []
    for account_id in warn_list:
        player_line = account_id
        if 'account name' in warn_list[account_id]:
            player_line += ' | ' + warn_list[account_id]['account name']
        warn_list_show.append(player_line)
        if 'until' in warn_list[account_id]:
            time_line = '       - варн до ' + translate_time(warn_list[account_id]['until'])
            warn_list_show.append(time_line)
        for i in range(len(warn_list[account_id]['reasons'])):
            reason_line = '      [' + str(i + 1) + '] причина: ' + warn_list[account_id]['reasons'][i]
            warn_list_show.append(reason_line)
    from chatCommands.chat_command_functions import show_pages
    showmessage(client_id, type, '=============== варн-лист: ===============', _white_)
    show_pages(client_id, warn_list_show, type, page)
