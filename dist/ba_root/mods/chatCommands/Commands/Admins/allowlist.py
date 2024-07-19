import os

import ba, _ba

aliases = ['givelist']
description = 'показать разрешения и запреты'
info = [
    '                     список разрешений и запретов',
    '                             /allowlist   [страница]'
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
    show_allowlist(client_id, type, page)

def show_allowlist(client_id, type, page):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    session.update_allow_data()
    allow_list = session.playersData['allow_data']
    from chatHandle.chat_functions import translate_time
    allow_list_show = []
    from chatHandle.chat_functions import string_type
    for allow in allow_list:
        if string_type(allow['subject']) == 'pb_id':
            allow_line = allow['subject']
            if allow['action'] != 'disallow':
                allow_line += ' | ' + allow['type']
            else:
                allow_line += ' | ' + 'запрещено: '
                if allow['type'] == 'free_role':
                    allow_line += 'роль за топ'
                else:
                    allow_line += allow['type']
            if 'subtype' in allow:
                allow_line += ' ' + allow['subtype']
            if 'count' in allow:
                allow_line += ' [' + str(allow['count']) + ']'
            if 'until' in allow:
                allow_line += ' до ' + translate_time(allow['until'])
            if allow['action'] == 'self_only':
                allow_line += ' [self only]'
            allow_list_show.append(allow_line)
    from chatCommands.chat_command_functions import show_pages
    showmessage(client_id, type, '=========== разрешения и запреты: ===========', _white_)
    show_pages(client_id, allow_list_show, type, page)
