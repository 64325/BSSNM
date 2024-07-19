import time

# импортируем модули ba и _ba
import ba, _ba

# алиасы для команды
aliases = ['take']
# описание команды
description = 'запретить команду'
# информация о команде
info = [
    '    запретить команду:',
    '    /take   команда [предмет]   номер игрока или pb-id',
    '    доп. параметры:',
    '    t=время ',
    '    запретить привилегию за топ:',
    '    /take free_role   номер игрока или pb-id'
]

# используем ли игровые ID игроков
using_players_ids = True
# используем ли pb-id
using_pb_ids = True

# импортируем необходимые модули из текущего пакета
from .. import Players, Admins, Creator

# функция для извлечения аргументов из команды
def extract_args(client_id, account_id, command):
    # импортируем необходимые функции из других модулей
    from chatHandle.chat_functions import showmessage, _red_
    from chatCommands.chat_command_functions import parse_time
    
    # проверяем наличие параметра времени 't'
    if 't' in command['keys'] and len(command['keys']['t']) == 1:
        try:
            # разбираем время и ограничиваем его до одного года
            value = min(365 * 24 * 60 * 60, max(1, parse_time(command['keys']['t'][0])))
            command['keys']['t'].pop(0)
            command['parsed_keys']['t'] = value
        except:
            return False
        command['keys'].pop('t')
    else:
        command['parsed_keys']['t'] = None
    
    # проверяем наличие ключа 'free_role' в аргументах
    if 'free_role' in command['args']:
        command['args'].remove('free_role')
        command['parsed_keys']['allow_type'] = 'free_role'
        return True
    
    # если аргументов нет, выводим сообщение об ошибке
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите название команды', _red_)
        return False
    
    # извлекаем тип разрешения (команды)
    allow_type = command['args'][0]
    command['args'].pop(0)
    command['parsed_keys']['allow_type'] = allow_type
    
    # проверяем наличие подтипа разрешения
    from chatHandle.chat_functions import string_type
    if len(command['args']) != 0 and (string_type(command['args'][0]) == 'name' or string_type(command['args'][0]) == 'notype') and command['args'][0] != 'a' and command['args'][0] != 'all' and command['args'][0] != 'me' and not command['args'][0].startswith('-'):
        allow_subtype = command['args'][0]
        command['args'].pop(0)
        command['parsed_keys']['allow_subtype'] = allow_subtype
    
    return True

# функция для выполнения команды
def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    # если разрешение - 'free_role', вызываем соответствующую функцию
    if command_keys['allow_type'] == 'free_role':
        disallow_free_role(client_id, account_id, type, pb_id, acc_name, command_keys['t'])
        return
    
    # определяем подтип разрешения, если он указан
    if 'allow_subtype' in command_keys:
        allow_subtype = command_keys['allow_subtype']
    else:
        allow_subtype = None
    
    # вызываем функцию для добавления запрета
    add_disallow(client_id, account_id, type, pb_id, acc_name, command_keys['allow_type'], allow_subtype, command_keys['t'])

# функция для запрета free_role
def disallow_free_role(client_id, account_id, type, pb_id, acc_name, time_interval):
    # импортируем необходимые функции и данные
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    from ModData.account_info import client_to_display_string
    
    # получаем отображаемое имя аккаунта
    account_name = client_to_display_string(client_id)
    session.update_allow_data()
    
    # проверяем, что аккаунт не пытается запретить себе free_role
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете выдавать себе команды', _red_)
        return
    
    # получаем роли аккаунтов
    from ModData.me import get_role, get_value
    account_role = get_role(account_id, account_name, client_id)
    account_value = get_value(account_role)
    player_value = get_value(get_role(pb_id))
    
    # проверяем статус аккаунта по отношению к игроку, которому нужно запретить free_role
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    
    # проверяем возможность редактировать запись о free_role
    for allow in session.playersData['allow_data']:
        if allow['subject'] == pb_id and allow['type'] == 'free_role' and 'admin' in allow:
            admin_value = get_value(get_role(allow['admin']))
            if account_value < admin_value:
                showmessage(client_id, type, 'вы не можете редактировать запись, созданную игроком ' + allow['admin'], _red_)
                return
    
    # логируем выполнение команды и добавляем запрет
    from chatCommands.chat_command_functions import log_command, add_cooldown
    log_command(account_id, 'disallow free_role', pb_id, '')
    from ModData import allow
    allow.execute_allow(pb_id, 'disallow', 'free_role', None, account_id, time.time(), time_interval, None, False)

# функция для добавления запрета на команду
def add_disallow(client_id, account_id, type, pb_id, acc_name, command_name, subtype, time_interval):
    # импортируем необходимые функции и данные
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    from ModData.account_info import client_to_display_string
    
    # получаем отображаемое имя аккаунта
    account_name = client_to_display_string(client_id)
    session.update_allow_data()
    
    # проверяем, что аккаунт не пытается запретить себе команду
    if pb_id == account_id:
        showmessage(client_id, type, 'вы не можете выдавать себе команды', _red_)
        return
    
    # получаем роли аккаунтов
    from ModData.me import get_role, get_value
    account_role = get_role(account_id, account_name, client_id)
    account_value = get_value(account_role)
    player_value = get_value(get_role(pb_id))
    
    # проверяем статус аккаунта по отношению к игроку, которому нужно запретить команду
    if account_value <= player_value:
        showmessage(client_id, type, 'ваш статус ниже чем у игрока ' + pb_id, _red_)
        return
    
    # проверяем существование команды и возможность её запрета
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
    
    # если команда не найдена, выводим сообщение об ошибке
    if command_submodule == None:
        if command_found:
            showmessage(client_id, type, 'вы не можете забирать эту команду', _red_)
            return
        showmessage(client_id, type, command_name + ': команда не найдена', _red_)
        return
    
    # проверяем подтип команды, если он указан
    if subtype != None:
        if not hasattr(command_submodule, 'subtypes') or subtype not in command_submodule.subtypes:
            showmessage(client_id, type, subtype + ': тип не найден', _red_)
            return
    
    # проверяем возможность редактировать запись о команде
    for allow in session.playersData['allow_data']:
        if allow['subject'] == pb_id and allow['type'] == command_name and ('subtype' not in allow or allow['subtype'] != subtype) and 'admin' in allow:
            admin_value = get_value(get_role(allow['admin']))
            if account_value < admin_value:
                showmessage(client_id, type, 'вы не можете редактировать запись, созданную игроком ' + allow['admin'], _red_)
                return
    
    # логируем выполнение команды и добавляем запрет
    from chatCommands.chat_command_functions import log_command, add_cooldown
    logstr = 'disallow ' + command_name
    if subtype != None:
        logstr += ' ' + subtype
    log_command(account_id, logstr, pb_id, '')
    from ModData import allow
    allow.execute_allow(pb_id, 'disallow', command_name, subtype, account_id, time.time(), time_interval, None, False)
    session.update_allow_data()
