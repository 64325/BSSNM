import time

import ba, _ba

description = 'выдать игроку статус'
info = [
]

using_players_ids = True
using_pb_ids = True
using_accounts_names = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    from chatCommands.chat_command_functions import parse_time
    if 'list' in command['args']:
        command['args'].remove('list')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            return False
        return True
    if 'l' in command['args']:
        command['args'].remove('l')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            return False
        return True
    command['parsed_keys']['action'] = 'set'
    if 't' in command['keys']:
        if len(command['keys']['t']) != 1:
            return False
        try:
            value = min(365 * 24 * 60 * 60, max(1, parse_time(command['keys']['t'][0])))
            command['keys']['t'].pop(0)
            command['parsed_keys']['t'] = value
        except:
            return False
        command['keys'].pop('t')
    elif 'forever' in command['args']:
        command['args'].remove('forever')
        command['parsed_keys']['t'] = None
    else:
        command['parsed_keys']['t'] = 30.0 * 24.0 * 60.0 * 60.0
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите статус', _red_)
        return False
    role_name = command['args'][0]
    command['args'].pop(0)
    if len(role_name) > 2 and role_name[0] == "'" and role_name[-1] == "'":
        role_name = role_name[1:-1]
    from chatHandle.chat_functions import string_type
    if string_type(role_name) != 'name' and string_type(role_name) != 'notype':
        showmessage(client_id, command['type'], 'такое название статуса использовать нельзя', _red_)
        return False
    command['parsed_keys']['role'] = role_name
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    from chatHandle.chat_functions import showmessage, _red_
    if command_keys['action'] == 'show':
        show_roles(client_id, type)
        return
    add_role(client_id, account_id, type, pb_id, acc_name, command_keys['t'], command_keys['role'])

def add_role(client_id, account_id, type, pb_id, acc_name, time_interval, role):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    from ModData.account_info import client_to_display_string
    account_name = client_to_display_string(client_id)
    if pb_id == None:
        from ModData.me import get_role, get_value
        account_value = get_value(get_role(account_id, account_name, client_id))
        from ModData.account_info import display_string_to_accounts
        accounts = display_string_to_accounts(acc_name)
        for acc_id in accounts:
            acc_value = get_value(get_role(acc_id))
            if account_value <= acc_value:
                showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + acc_name, _red_)
                return
        role_value = get_value(role)
        if account_value <= role_value:
            showmessage(client_id, type, 'вы не можете выдавать эту привилегию', _red_)
            return
        from chatCommands.chat_command_functions import log_command, add_cooldown
        log_command(account_id, 'setstatus ' + role, acc_name, '')
        from ModData import roles
        if role == 'PLAYER':
            roles.remove_role(acc_name)
        else:
            roles.add_role(acc_name, acc_name, role, time.time(), time_interval)
        session.update_roles()
        return
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете выдавать себе привилегии', _red_)
        return
    from ModData.me import get_role, get_value
    account_value = get_value(get_role(account_id, account_name, client_id))
    player_value = get_value(get_role(pb_id, acc_name))
    role_value = get_value(role)
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    if account_value <= role_value:
        showmessage(client_id, type, 'вы не можете выдавать эту привилегию', _red_)
        return
    from chatCommands.chat_command_functions import log_command, add_cooldown
    log_command(account_id, 'setstatus ' + role, pb_id, '')
    from ModData import roles
    if role == 'PLAYER':
        roles.remove_role(pb_id)
    else:
        roles.add_role(pb_id, acc_name, role, time.time(), time_interval)
    session.update_roles()

def show_roles(client_id, type):
    type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    showmessage(client_id, type, '=============== привилегии: ===============', _white_)
    for status in session.serverData['server_roles']:
        if status != 'PLAYER' and status != 'CREATOR':
            showmessage(client_id, type, '    ' + status, _white_)
