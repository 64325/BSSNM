import time

import ba, _ba

description = 'выдать игроку мут'
info = [
    '   /mute   номер игрока, pb-id или аккаунт   [t=период]   [причина]',
    '                /mute 118 t=1h30min шутит про мамку'
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
    add_mute(client_id, account_id, type, pb_id, acc_name, time_interval, command_keys['string_arg'])

def add_mute(client_id, account_id, type, pb_id, acc_name, time_interval, reason):
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
        session.update_mutelist()
        if acc_name in session.playersData['mutelist']:
            if 'banned by' in session.playersData['mutelist'][acc_name]:
                admin_id = session.playersData['mutelist'][acc_name]['banned by']
                admin_value = get_value(get_role(admin_id))
                if account_value < admin_value:
                    showmessage(client_id, type, 'аккаунту уже выдан мут админом ' + admin_id, _red_)
                    return
        #if reason == '':
        #    showmessage(client_id, type, 'нужно указать причину мута', _red_)
        #    return
        from chatCommands.chat_command_functions import log_command, add_cooldown
        from chatHandle.chat_functions import translate_time
        if time_interval == None:
            log_command(account_id, 'mute', acc_name, '')
        else:
            log_command(account_id, 'mute', acc_name, 'до ' + translate_time(time.ctime(time.time() + time_interval)))
        from ModData import mute
        mute.add_mute(acc_name, acc_name, account_id, reason, time.time(), time_interval)
        session.update_mutelist()
        return
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете мутить себя', _red_)
        return
    from ModData.me import get_role, get_value
    account_value = get_value(get_role(account_id, account_name, client_id))
    player_value = get_value(get_role(pb_id, acc_name))
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    session.update_mutelist()
    if pb_id in session.playersData['mutelist']:
        if 'muted by' in session.playersData['mutelist'][pb_id]:
            admin_id = session.playersData['mutelist'][pb_id]['muted by']
            admin_value = get_value(get_role(admin_id))
            if account_value < admin_value:
                showmessage(client_id, type, 'игроку уже выдан мут админом ' + admin_id, _red_)
                return
    #if reason == '':
    #    showmessage(client_id, type, 'нужно указать причину мута', _red_)
    #    return
    from chatCommands.chat_command_functions import log_command, add_cooldown
    from chatHandle.chat_functions import translate_time
    if time_interval == None:
        log_command(account_id, 'mute', pb_id, '')
    else:
        log_command(account_id, 'mute', pb_id, 'до ' + translate_time(time.ctime(time.time() + time_interval)))
    from ModData import mute
    mute.add_mute(pb_id, acc_name, account_id, reason, time.time(), time_interval)
    session.update_mutelist()
