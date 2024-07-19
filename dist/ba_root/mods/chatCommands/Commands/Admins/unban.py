import time

import ba, _ba

description = 'разбанить игрока'
info = [
    '                                  разбанить игрока',
    '              /unban   номер игрока, pb-id или аккаунт'
]

using_players_ids = True
using_pb_ids = True
using_accounts_names = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    remove_ban(client_id, account_id, type, pb_id, acc_name)

def remove_ban(client_id, account_id, type, pb_id, acc_name):
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
                    showmessage(client_id, type, 'аккаунту выдан бан админом ' + admin_id, _red_)
                    return
        else:
            showmessage(client_id, type, 'аккаунта ' + acc_name + ' нет в бан-листе', _red_)
            return
        from chatCommands.chat_command_functions import log_command, add_cooldown
        from chatHandle.chat_functions import translate_time
        log_command(account_id, 'unban', acc_name, '')
        from ModData import ban
        ban.remove_ban(acc_name)
        session.update_banlist()
        return
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете разбанить себя', _red_)
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
                showmessage(client_id, type, 'игроку выдан бан админом ' + admin_id, _red_)
                return
    else:
        showmessage(client_id, type, 'игрока ' + pb_id + ' нет в бан-листе', _red_)
        return
    from chatCommands.chat_command_functions import log_command, add_cooldown
    from chatHandle.chat_functions import translate_time
    log_command(account_id, 'unban', pb_id, '')
    from ModData import ban
    ban.remove_ban(pb_id)
    session.update_banlist()
