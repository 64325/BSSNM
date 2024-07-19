import time

import ba, _ba

description = 'забанить игрока'
info = [
    '    /ban   номер игрока, pb-id или аккаунт   [t=период]   [причина]',
    '                    /ban 115 t=5d играет лучше меня'
]

using_players_ids = True
using_pb_ids = True
using_accounts_names = True
using_string_arg = True

def extract_args(client_id, account_id, command):
    from chatCommands.chat_command_functions import parse_time
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
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    if 't' in command_keys:
        time_interval = command_keys['t']
    else:
        time_interval = None
    add_ban(client_id, account_id, type, pb_id, acc_name, time_interval, command_keys['string_arg'])

def add_ban(client_id, account_id, type, pb_id, acc_name, time_interval, reason):
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
        session.update_banlist()
        if acc_name in session.playersData['banlist']:
            if 'banned by' in session.playersData['banlist'][acc_name]:
                admin_id = session.playersData['banlist'][acc_name]['banned by']
                admin_value = get_value(get_role(admin_id))
                if account_value < admin_value:
                    showmessage(client_id, type, 'аккаунту уже выдан бан админом ' + admin_id, _red_)
                    return
        #if reason == '':
        #    showmessage(client_id, type, 'нужно указать причину бана', _red_)
        #    return
        from chatCommands.chat_command_functions import log_command, add_cooldown
        from chatHandle.chat_functions import translate_time
        if time_interval == None:
            log_command(account_id, 'ban', acc_name, '')
        else:
            log_command(account_id, 'ban', acc_name, 'до ' + translate_time(time.ctime(time.time() + time_interval)))
        from ModData import ban
        ban.add_ban(acc_name, acc_name, account_id, reason, time.time(), time_interval)
        session.update_banlist()
        return
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете банить себя', _red_)
        return
    from ModData.me import get_role, get_value
    account_value = get_value(get_role(account_id, account_name, client_id))
    player_value = get_value(get_role(pb_id, acc_name))
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    session.update_banlist()
    if pb_id in session.playersData['banlist']:
        if 'banned by' in session.playersData['banlist'][pb_id]:
            admin_id = session.playersData['banlist'][pb_id]['banned by']
            admin_value = get_value(get_role(admin_id))
            if account_value < admin_value:
                showmessage(client_id, type, 'игроку уже выдан бан админом ' + admin_id, _red_)
                return
    #if reason == '':
    #    showmessage(client_id, type, 'нужно указать причину бана', _red_)
    #    return
    from chatCommands.chat_command_functions import log_command, add_cooldown
    from chatHandle.chat_functions import translate_time
    if time_interval == None:
        log_command(account_id, 'ban', pb_id, '')
    else:
        log_command(account_id, 'ban', pb_id, 'до ' + translate_time(time.ctime(time.time() + time_interval)))
    from ModData import ban
    ban.add_ban(pb_id, acc_name, account_id, reason, time.time(), time_interval)
    session.update_banlist()
