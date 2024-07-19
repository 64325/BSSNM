import time

import ba, _ba

# Псевдонимы для команды
aliases = ['def']
# Описание команды
description = 'удалить разрешение/запрет'
# Информация о команде
info = [
    '    сбросить разрешение:',
    '    /default   команда [предмет]   номер игрока или pb-id',
    '    разрешить привилегию за топ:',
    '    /default free_role   номер игрока или pb-id'
]

# Использование идентификаторов игроков
using_players_ids = True
# Использование pb-идентификаторов
using_pb_ids = True

from .. import Players, Admins, Creator

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    
    # Проверка на параметр free_role
    if 'free_role' in command['args']:
        command['args'].remove('free_role')
        command['parsed_keys']['allow_type'] = 'free_role'
        return True
    
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
    if len(command['args']) != 0 and (string_type(command['args'][0]) == 'name' or string_type(command['args'][0]) == 'notype') and command['args'][0] != 'a' и command['args'][0] != 'all' and command['args'][0] != 'me' and not command['args'][0].startswith('-'):
        allow_subtype = command['args'][0]
        command['args'].pop(0)
        command['parsed_keys']['allow_subtype'] = allow_subtype
    
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    # Проверка типа free_role
    if command_keys['allow_type'] == 'free_role':
        allow_free_role(client_id, account_id, type, pb_id, acc_name)
        return
    
    # Проверка наличия подтипа
    if 'allow_subtype' in command_keys:
        subtype = command_keys['allow_subtype']
    else:
        subtype = None
    
    # Установка по умолчанию
    set_default(client_id, account_id, type, pb_id, acc_name, command_keys['allow_type'], subtype)

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
    
    # Логирование команды
    log_command(account_id, 'allow free_role', pb_id, '')
    from ModData import allow
    allow.execute_allow(pb_id, 'default', 'free_role', None, account_id, time.time(), None, None, False)

# Функция для установки по умолчанию
def set_default(client_id, account_id, type, pb_id, acc_name, command_name, subtype):
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
    logstr = 'default ' + command_name
    if subtype != None:
        logstr += ' ' + subtype
    
    log_command(account_id, logstr, pb_id, '')
    
    from ModData import allow
    allow.execute_allow(pb_id, 'default', command_name, subtype, account_id, time.time(), None, None, False)
    session.update_allow_data()
