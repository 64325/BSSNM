import time

import ba, _ba

description = 'размутить игрока'
info = [
    '                                  размутить игрока',
    '              /unmute   номер игрока, pb-id или аккаунт'
]

using_players_ids = True
using_pb_ids = True
using_accounts_names = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    remove_mute(client_id, account_id, type, pb_id, acc_name)

def remove_mute(client_id, account_id, type, pb_id, acc_name):
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
            if 'muted by' in session.playersData['mutelist'][acc_name]:
                admin_id = session.playersData['mutelist'][acc_name]['muted by']
                admin_value = get_value(get_role(admin_id))
                if account_value < admin_value:
                    showmessage(client_id, type, 'аккаунту выдан мут админом ' + admin_id, _red_)
                    return
        else:
            showmessage(client_id, type, 'аккаунта ' + acc_name + ' нет в мут-листе', _red_)
            return
        from chatCommands.chat_command_functions import log_command, add_cooldown
        from chatHandle.chat_functions import translate_time
        log_command(account_id, 'unmute', acc_name, '')
        from ModData import mute
        mute.remove_mute(acc_name)
        session.update_mutelist()
        return
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете размутить себя', _red_)
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
                showmessage(client_id, type, 'игроку выдан мут админом ' + admin_id, _red_)
                return
    else:
        showmessage(client_id, type, 'игрока ' + pb_id + ' нет в мут-листе', _red_)
        return
    from chatCommands.chat_command_functions import log_command, add_cooldown
    from chatHandle.chat_functions import translate_time
    log_command(account_id, 'unmute', pb_id, '')
    from ModData import mute
    mute.remove_mute(pb_id)
    session.update_mutelist()
