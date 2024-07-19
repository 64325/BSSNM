from __future__ import annotations

from typing import TYPE_CHECKING

import os

import _ba, ba
import time

from ModData.account_info import client_to_account, client_to_display_string, client_to_player
from ModData.strings import *
from chatHandle.chat_functions import string_type, showmessage

_red_ = (1.0, 0.1, 0.0)
_white_ = (0.9, 0.9, 0.9)
_black_ = (0.0, 0.0, 0.0)
_light_yellow_ = (1.0, 0.85, 0.3)
_light_green_ = (0.5, 1.0, 0.5)
_yellow_ = (1.0, 1.0, 0.0)

# Нормализация имени команды
def normalise_command_name(client_id, account_id, command, command_module):
    if command['name'] not in command_module.__all__:
        for name in command_module.__all__:
            command_attr = getattr(command_module, name)
            if hasattr(command_attr, 'aliases') and command['name'] in command_attr.aliases:
                command['name'] = name
                break

# Проверка разрешений для выполнения команды
def check_permission(client_id, account_id, account_name, command_name, command_module):
    session = _ba.get_foreground_host_session()
    if command_name not in command_module.__all__:
        for name in command_module.__all__:
            command_attr = getattr(command_module, name)
            if hasattr(command_attr, 'aliases') and command_name in command_attr.aliases:
                command_name = name
                break
    check_result = 'allow' if command_module.check_permission(client_id, account_id, account_name, command_name) else 'disallow'
    
    # Получение роли пользователя
    from ModData.me import get_role
    role = get_role(account_id, account_name, client_id)
    
    # Получение ранга пользователя
    from ModData.ranking import get_rank, in_rating
    rank = get_rank(account_id) if in_rating(account_id) else None
    
    # Получение статуса разрешения
    from ModData.allow import get_allow_status
    allow_result = get_allow_status(session.playersData['allow_data'], role, rank, account_id, command_name, default=check_result)
    
    return allow_result != 'disallow'

# Выполнение команды
def execute(client_id, account_id, account_name, command, command_module):
    session = _ba.get_foreground_host_session()
    normalise_command_name(client_id, account_id, command, command_module)
    command_submodule = getattr(command_module, command['name'])

    if len(command['args']) == 1 and 'help' in command['args']:
        show_info(client_id, command_submodule)
        return
    elif len(command['args']) == 1 and 'h' in command['args']:
        show_info(client_id, command_submodule)
        return

    name0 = command['name']
    command['parsed_keys'] = {}
    if hasattr(command_submodule, 'subtypes'):
        command['subtype'] = ''
    if not command_submodule.extract_args(client_id, account_id, command):
        showmessage(client_id, command['type'], args_error_str, _red_)
        return 'error'

    session.update_allow_data()
    check_result = 'allow' if (command['permitted'] or command_module.check_permission(client_id, account_id, account_name, name0)) else 'disallow'
    
    # Получение роли пользователя
    from ModData.me import get_role
    role = get_role(account_id, account_name, client_id)
    
    # Получение ранга пользователя
    from ModData.ranking import get_rank
    rank = get_rank(account_id)
    
    # Получение статуса разрешения
    from ModData.allow import get_allow_status, use_allow
    session = _ba.get_foreground_host_session()
    if hasattr(command_submodule, 'subtypes'):
        allow_result = get_allow_status(session.playersData['allow_data'], role, rank, account_id, name0, command['subtype'], default=check_result)
    else:
        allow_result = get_allow_status(session.playersData['allow_data'], role, rank, account_id, name0, default=check_result)
    
    if allow_result == 'disallow':
        showmessage(client_id, command['type'], permission_denied_str, _red_)
        return
    
    if 'subtype' in command:
        try:
            use_allow(account_id, name0, command['subtype'])
        except:
            pass
    else:
        try:
            use_allow(account_id, name0)
        except:
            pass
    
    if allow_result == 'self_only':
        command['self_only'] = True
    
    if command['name'] != name0:
        return 'change'
    
    if len(command['keys']) != 0:
        showmessage(client_id, command['type'], args_error_str, _red_)
        return
    
    command['permitted'] = None
    command['players'] = []
    command['pb_ids'] = []
    command['accounts_names'] = []
    
    use_players_ids = hasattr(command_submodule, 'using_players_ids') and command_submodule.using_players_ids
    use_pb_ids = hasattr(command_submodule, 'using_pb_ids') and command_submodule.using_pb_ids
    use_accounts_names = hasattr(command_submodule, 'using_accounts_names') and command_submodule.using_accounts_names
    
    if use_players_ids:
        get_players_list(client_id, command, use_pb_ids=use_pb_ids, use_accounts_names=use_accounts_names)
        
        if 'self_only' in command and (len(command['players']) != 0 and client_id not in command['players'] or len(command['players']) > 1):
            showmessage(client_id, command['type'], self_only_str, _red_)
            return
        
        if 'self_only' in command and (len(command['pb_ids']) != 0 and account_id not in command['pb_ids'] or len(command['pb_ids']) > 1):
            showmessage(client_id, command['type'], self_only_str, _red_)
            return
        
        if 'self_only' in command and len(command['accounts_names']) != 0:
            showmessage(client_id, command['type'], self_only_str, _red_)
            return
    
    if hasattr(command_submodule, 'using_string_arg') and command_submodule.using_string_arg:
        command['parsed_keys']['string_arg'] = extract_string_arg(command)
        if len(command['parsed_keys']['string_arg']) >= 2 and command['parsed_keys']['string_arg'][0] == "'" and command['parsed_keys']['string_arg'][-1] == "'":
            command['parsed_keys']['string_arg'] = command['parsed_keys']['string_arg'][1:-1]
    
    if len(command['args']) != 0:
        showmessage(client_id, command['type'], args_error_str, _red_)
        return
    
    if use_players_ids:
        for player in (command['players'] + command['pb_ids']):
            if use_pb_ids:
                if player in session.playersData['stats'] and len(session.playersData['stats'][player]['account name']) != 0:
                    account_name = session.playersData['stats'][player]['account name'][-1]
                else:
                    account_name = ''
                run_command_or_start_timer(client_id, account_id, command, command_submodule, player, account_name)
            else:
                run_command_or_start_timer(client_id, account_id, command, command_submodule, player)
        
        if use_accounts_names:
            for player in (command['accounts_names']):
                run_command_or_start_timer(client_id, account_id, command, command_submodule, None, player)
    
    else:
        run_command_or_start_timer(client_id, account_id, command, command_submodule)

def run_command_or_start_timer(client_id, account_id, command, command_submodule, player=None, account_name=None):
    with ba.Context(_ba.get_foreground_host_activity()):
        if 'is_delayed' in command:
            if not hasattr(command_submodule, 'timer_compatible') or not command_submodule.timer_compatible:
                showmessage(client_id, command['type'], timer_not_compatible_str, _red_)
            else:
                activity = ba.getactivity()
                try:
                    if activity.globalsnode.slow_motion:
                        command['timer_interval'] /= 3.0
                except:
                    pass
                
                session = activity.session
                if not hasattr(session, 'commandsTimers'): session.commandsTimers = []
                
                session.commandsTimers.append(ba.Timer(command['timer_interval'], ba.Call(run_command, client_id, account_id, command, command_submodule, player, account_name)))
        
        elif 'repeat' in command:
            if not hasattr(command_submodule, 'timer_compatible') or not command_submodule.timer_compatible:
                showmessage(client_id, command['type'], timer_not_compatible_str, _red_)
            else:
                activity = ba.getactivity()
                try:
                    if activity.globalsnode.slow_motion:
                        command['timer_interval'] /= 3.0
                        if 'timer_offset' in command:
                            command['timer_offset'] /= 3.0
                except:
                    pass
                
                if 'timer_offset' in command:
                    cur_time = ba.time()
                    k = int(cur_time / command['timer_interval']) - 1
                    start_time = k * command['timer_interval'] + command['timer_offset']
                    
                    while (start_time <= cur_time):
                        start_time += command['timer_interval']
                    
                    command['start_time'] = start_time
                    session = activity.session
                    if not hasattr(session, 'commandsTimers'): session.commandsTimers = []
                    session.commandsTimers.append(ba.Timer(max(0.001, start_time - cur_time - 0.04), ba.Call(start_timer, client_id, account_id, command, command_submodule, player, account_name)))
                
                else:
                    start_timer(client_id, account_id, command, command_submodule, player, account_name)
        
        else:
            run_command(client_id, account_id, command, command_submodule, player, account_name)

def start_timer(client_id, account_id, command, command_submodule, player=None, account_name=None):
    if 'timer_offset' in command:
        if command['start_time'] - ba.time() > 0.01:
            ba.timer(0.001, ba.Call(start_timer, client_id, account_id, command, command_submodule, player, account_name))
            return
    
    session = _ba.get_foreground_host_session()
    if not hasattr(session, 'commandsTimers'): session.commandsTimers = []
    
    run_command(client_id, account_id, command, command_submodule, player, account_name, called_from_timer=True)
    
    session.commandsTimers.append(ba.Timer(command['timer_interval'], ba.Call(run_command, client_id, account_id, command, command_submodule, player, account_name, True), repeat=True))

def run_command(client_id, account_id, command, command_submodule, player=None, account_name=None, called_from_timer=False):
    session = _ba.get_foreground_host_session()
    
    if account_id in session.playersData['cooldown'] and command['name'] in session.playersData['cooldown'][account_id]:
        time_interval = int(session.playersData['cooldown'][account_id][command['name']] - time.time())
        
        if time_interval > 0:
            time_str = ''
            if time_interval > 60:
                time_str += str(int(time_interval / 60)) + ' мин '
            time_str += str(time_interval % 60) + ' сек'
            showmessage(client_id, 2, 'команда будет доступна через ' + time_str, _yellow_)
            return
        
        else:
            session.playersData['cooldown'][account_id].pop(command['name'])
    
    if called_from_timer and hasattr(command_submodule, 'run_command_timer_on'):
        if player == None:
            command_submodule.run_command_timer_on(client_id, account_id, command['type'], command['parsed_keys'])
        elif account_name == None:
            command_submodule.run_command_timer_on(client_id, account_id, command['type'], command['parsed_keys'], player)
        else:
            command_submodule.run_command_timer_on(client_id, account_id, command['type'], command['parsed_keys'], player, account_name)
    
    else:
        if player == None and account_name == None:
            command_submodule.run_command(client_id, account_id, command['type'], command['parsed_keys'])
        elif account_name == None:
            command_submodule.run_command(client_id, account_id, command['type'], command['parsed_keys'], player)
        else:
            command_submodule.run_command(client_id, account_id, command['type'], command['parsed_keys'], player, account_name)

def show_info(client_id, command_submodule):
    from chatHandle.chat_functions import _white_
    if hasattr(command_submodule, 'info'):
        command_name = command_submodule.__name__.split('.')[-1]
        showmessage(client_id, 3, '                        ' + ' ' * max(0, 20 - len(command_name)) + '<< ' + command_name + ' >>', _white_)
        for info_line in command_submodule.info:
            showmessage(client_id, 3, info_line, _white_)
    else:
        showmessage(client_id, 3, '                              << ' + command_submodule.__name__.split('.')[-1] + ' >>', _white_)
        showmessage(client_id, 3, '        ' + command_submodule.description, _white_)

def get_players_list(client_id, command, use_pb_ids = False, use_accounts_names = False):
    players_list = []
    pb_ids = []
    accounts_names = []
    _remove = []
    players_error = []
    
    rost = _ba.get_game_roster()
    clients = []
    for i in rost:
        clients.append(i['client_id'])
    if -1 in clients: clients.remove(-1)
    
    while len(command['args']) > 0:
        arg = command['args'][0]
        try:
            if use_pb_ids and string_type(arg) == 'pb_id':
                if not arg in pb_ids: pb_ids.append(arg)
            elif use_accounts_names and string_type(arg) == 'account_name':
                if not arg in accounts_names: accounts_names.append(arg)
            elif arg == 'all' or arg == 'a':
                for client in clients:
                    if not client in players_list: players_list.append(client)
            elif arg == 'me': players_list.append(client_id)
            elif arg == '-me': _remove.append(client_id)
            elif arg[0] == '-':
                player = int(arg[1:])
                if not player in _remove: _remove.append(player)
            else:
                player = int(arg)
                if not player in players_list:
                    if player in clients: players_list.append(player)
                    elif not player in players_error: players_error.append(player)
        except:
            break
        
        command['args'].pop(0)
    
    if len(players_list) == 0 and len(pb_ids) == 0 and len(accounts_names) == 0 and len(players_error) == 0 and len(_remove) == 0:
        players_list.append(client_id)
    
    for player in _remove:
        if player in players_list: players_list.remove(player)
    
    for player in players_list:
        acc_id = client_to_account(player)
        if acc_id in pb_ids:
            pb_ids.remove(acc_id)
    
    for player in players_error:
        showmessage(client_id, command['type'], str(player) + ': ' + player_not_found_str, _red_)
    
    if use_pb_ids:
        for player in players_list:
            account_id = client_to_account(player)
            if account_id != '':
                pb_ids.append(account_id)
        players_list = []
    
    if client_id in players_list:
        players_list.remove(client_id)
        players_list.append(client_id)
    
    command['players'] = players_list
    command['pb_ids'] = pb_ids
    command['accounts_names'] = accounts_names

def extract_string_arg(command):
    string_arg = ''
    while len(command['args']) > 0:
        if string_arg != '': string_arg += ' '
        if len(command['args'][0]) >= 2 and command['args'][0][0] == "'" and command['args'][0][-1] == "'":
            string_arg += command['args'][0][1:-1]
        else:
            string_arg += command['args'][0]
        command['args'].pop(0)
    return string_arg
