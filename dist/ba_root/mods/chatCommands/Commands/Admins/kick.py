import time

import ba, _ba

description = 'кикнуть игрока'
info = [
    '                                    кикнуть игрока',
    '                       /kick   номер игрока   [t=время]'
]

using_players_ids = True
using_string_arg = True

def extract_args(client_id, account_id, command):
    from chatCommands.chat_command_functions import parse_time
    if 't' in command['keys']:
        if len(command['keys']['t']) != 1:
            return False
        try:
            value = min(24 * 60 * 60, max(1, int(parse_time(command['keys']['t'][0]))))
            command['keys']['t'].pop(0)
            command['parsed_keys']['t'] = value
        except:
            return False
        command['keys'].pop('t')
    return True

def run_command(client_id, account_id, type, command_keys, player):
    if 't' in command_keys:
        time_interval = command_keys['t']
    else:
        time_interval = None
    kick_player(client_id, account_id, type, player, time_interval, command_keys['string_arg'])

def kick_player(client_id, account_id, type, cl_id, time_interval, reason):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    from ModData.account_info import client_to_display_string
    account_name = client_to_display_string(client_id)
    if cl_id == client_id:
        showmessage(client_id, type, 'вы не можете кикать себя', _red_)
        return
    from ModData.me import get_role, get_value
    account_value = get_value(get_role(account_id, account_name, client_id))
    from ModData.account_info import client_to_account, client_to_display_string
    acc_id = client_to_account(cl_id)
    acc_name = client_to_display_string(cl_id)
    player_value = get_value(get_role(acc_id, acc_name))
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + acc_id, _red_)
        return
    #if reason == '':
    #    showmessage(client_id, type, 'нужно указать причину кика', _red_)
    #    return
    from chatCommands.chat_command_functions import log_command, add_cooldown
    log_command(account_id, 'kick', acc_id, '')
    showmessage(cl_id, 2, 'вас кикнули', _red_)
    if reason != '':
        showmessage(cl_id, 2, reason, _red_)
    if time_interval == None:
        _ba.disconnect_client(client_id=cl_id)
    else:
        _ba.disconnect_client(client_id=cl_id, ban_time=time_interval)
