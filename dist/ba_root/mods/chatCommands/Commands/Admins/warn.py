import time

import ba, _ba

description = 'выдать предупреждение'

using_players_ids = True
using_pb_ids = True
using_string_arg = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    add_warn(client_id, account_id, type, pb_id, acc_name, command_keys['string_arg'])

def add_warn(client_id, account_id, type, pb_id, acc_name, reason):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    from ModData.account_info import client_to_display_string
    account_name = client_to_display_string(client_id)
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете выдавать себе варн', _red_)
        return
    from ModData.me import get_role, get_value
    account_value = get_value(get_role(account_id, account_name, client_id))
    player_value = get_value(get_role(pb_id))
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    session.update_warnlist()
    session.update_banlist()
    if pb_id in session.playersData['banlist']:
        showmessage(client_id, type, 'игрок находится в бане', _red_)
        return
    if reason == '':
        showmessage(client_id, type, 'нужно указать причину варна', _red_)
        return
    from chatCommands.chat_command_functions import log_command, add_cooldown
    log_command(account_id, 'warn', pb_id)
    from ModData import warn, ban, waiting_message
    warn.add_warn(pb_id, acc_name, reason, time.time(), 30.0 * 24.0 * 60.0 * 60.0)
    session.update_warnlist()
    if pb_id in session.playersData['warnlist'] and session.playersData['warnlist'][pb_id]['count'] >= 3:
        warn.remove_warn(pb_id)
        ban.add_ban(pb_id, acc_name, account_id, reason, time.time(), 30.0 * 24.0 * 60.0 * 60.0)
    else:
        waiting_message.add_message(pb_id, acc_name, 'вам выдано предупреждение', _red_, time.time())
        if reason != '':
            waiting_message.add_message(pb_id, acc_name, 'причина: ' + reason, _red_, time.time())
    session.update_warnlist()
    session.update_banlist()
    session.update_waiting_messages()
