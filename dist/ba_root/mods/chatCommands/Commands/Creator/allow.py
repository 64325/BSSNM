import time

import ba, _ba

# Псевдонимы для команды
aliases = ['give']
# Описание команды
description = 'выдать команду'
# Информация о команде
info = [
    '    выдать команду:',
    '    /give   команда [предмет]   номер игрока или pb-id',
    '    доп. параметры:',
    '    t=время   c=количество',
    '    self_only  -  использовать только для себя'
]

# Использование идентификаторов игроков
using_players_ids = True
# Использование pb-идентификаторов
using_pb_ids = True

from .. import Players, Admins, Creator

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    from chatCommands.chat_command_functions import parse_time
    
    # Проверка и парсинг времени
    if 't' in command['keys'] and len(command['keys']['t']) == 1:
        try:
            value = min(365 * 24 * 60 * 60, max(1, parse_time(command['keys']['t'][0])))
            command['keys']['t'].pop(0)
            command['parsed_keys']['t'] = value
        except:
            return False
        command['keys'].pop('t')
    else:
        command['parsed_keys']['t'] = None
    
    # Проверка на параметр free_role
    if 'free_role' in command['args']:
        command['args'].remove('free_role')
        command['parsed_keys']['allow_type'] = 'free_role'
        return True
    
    # Проверка на параметр self_only
    if 'self_only' in command['args']:
        command['args'].remove('self_only')
        command['parsed_keys']['self_only'] = True
    
    # Проверка наличия команды
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите название команды', _red_)
        return False
    
    # Извлечение типа команды
    allow_type = command['args'][0]
    command['args'].pop(0)
    command['parsed_keys']['allow_type'] = allow_type
    
    from chatHandle.chat_functions import string_type
    
    # Проверка и извлечение подтипа команды
    if len(command['args']) != 0 and (string_type(command['args'][0]) == 'name' or string_type(command['args'][0]) == 'notype') and command['args'][0] != 'a' and command['args'][0] != 'all' and command['args'][0] != 'me' and not command['args'][0].startswith('-'):
        allow_subtype = command['args'][0]
        command['args'].pop(0)
        command['parsed_keys']['allow_subtype'] = allow_subtype
    
    # Проверка и парсинг количества
    if 'c' in command['keys'] and len(command['keys']['c']) == 1:
        try:
            count = int(command['keys']['c'][0])
            if count <= 0:
                return 0
            command['parsed_keys']['count'] = min(1000000, count)
            command['keys'].pop('c')
        except:
            return False
    else:
        command['parsed_keys']['count'] = None
    
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    # Проверка типа free_role
    if command_keys['allow_type'] == 'free_role':
        allow_free_role(client_id, account_id, type, pb_id, acc_name)
        return
    
    # Проверка наличия подтипа
    if 'allow_subtype' in command_keys:
        allow_subtype = command_keys['allow_subtype']
    else:
        allow_subtype = None
    
    # Проверка self_only
    self_only = 'self_only' in command_keys and command_keys['self_only']
    
    # Добавление разрешения
    add_allow(client_id, account_id, type, pb_id, acc_name, command_keys['allow_type'], allow_subtype, command_keys['t'], command_keys['count'], self_only)

# Функция для разрешения free_role
def allow_free_role(client_id, account_id, type, pb_id, acc_name):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    from ModData.account_info import client_to_display_string
    
    account_name = client_to_display_string(client_id)
    session.update_allow_data()
    
    # Проверка, чтобы не выдавать команды самому себе
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете выдавать себе команды', _red_)
        return
    
    from ModData.me import get_role, get_value
    
    account_role = get_role(account_id, account_name, client_id)
    account_value = get_value(account_role)
    player_value = get_value(get_role(pb_id))
    
    # Проверка статуса игрока
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    
    # Проверка существующих разрешений
    for allow in session.playersData['allow_data']:
        if allow['subject'] == pb_id and allow['type'] == 'free_role' and 'admin' in allow:
            admin_value = get_value(get_role(allow['admin']))
            if account_value < admin_value:
                showmessage(client_id, type, 'вы не можете редактировать запись, созданную игроком ' + allow['admin'], _red_)
                return
    
    from chatCommands.chat_command_functions import log_command, add_cooldown
    
    log_command(account_id, 'allow free_role', pb_id, '')
    from ModData import allow
    allow.execute_allow(pb_id, 'default', 'free_role', None, account_id, time.time(), None, None, False)

# Функция для добавления разрешения
def add_allow(client_id, account_id, type, pb_id, acc_name, command_name, subtype, time_interval, count, self_only):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    from ModData.account_info import client_to_display_string
    
    account_name = client_to_display_string(client_id)
    session.update_allow_data()
    
    # Проверка, чтобы не выдавать команды самому себе
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете выдавать себе команды', _red_)
        return
    
    from ModData.me import get_role, get_value
    
    account_role = get_role(account_id, account_name, client_id)
    account_value = get_value(account_role)
    player_value = get_value(get_role(pb_id))
    
    # Проверка статуса игрока
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    
    # Поиск команды в модулях
    command_found = False
    command_submodule = None
    for command_module in [Players, Admins, Creator]:
        if command_name in command_module.__all__:
            command_found = True
            try:
                if command_module.check_permission(client_id, account_id, account_name, command_name):
                    command_submodule = getattr(command_module, command_name)
            except:
                pass
    
    # Проверка возможности выдачи команды
    if command_submodule == None:
        if command_found:
            showmessage(client_id, type, 'вы не можете выдавать эту команду', _red_)
            return
        showmessage(client_id, type, command_name + ': команда не найдена', _red_)
        return
    
    # Проверка наличия подтипа
    if subtype != None:
        if not hasattr(command_submodule, 'subtypes') or subtype not in command_submodule.subtypes:
            showmessage(client_id, type, subtype + ': тип не найден', _red_)
            return
    
    # Проверка существующих разрешений
    for allow in session.playersData['allow_data']:
        if allow['subject'] == pb_id and allow['type'] == command_name and ('subtype' not in allow or allow['subtype'] != subtype) and 'admin' in allow:
            admin_value = get_value(get_role(allow['admin']))
            if account_value < admin_value:
                showmessage(client_id, type, 'вы не можете редактировать запись, созданную игроком ' + allow['admin'], _red_)
                return
    
    from chatCommands.chat_command_functions import log_command, add_cooldown
    
    # Логирование команды
    logstr = 'allow ' + command_name
    if subtype != None:
        logstr += ' ' + subtype
    
    comment = ''
    if count != None:
        comment += ' c=' + str(count)
    if self_only:
        comment += ' self_only'
    
    log_command(account_id, logstr, pb_id, comment)
    
    from ModData import allow
    allow.execute_allow(pb_id, 'allow', command_name, subtype, account_id, time.time(), time_interval, count, self_only)
    session.update_allow_data()
