import os

import ba, _ba

# Определение алиасов и описания команды
aliases = ['help', 'h']
description = 'показать список команд'

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    if len(command['args']) != 0:
        try:
            value = int(command['args'][0])  # Пробуем преобразовать первый аргумент в число
            command['args'].pop(0)  # Удаляем первый аргумент из списка
        except:
            return False  # Возвращаем False, если преобразование не удалось
        command['parsed_keys']['page'] = max(0, value)  # Устанавливаем страницу, если преобразование удалось
    return True  # Возвращаем True, если аргументы успешно извлечены

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys):
    from chatCommands.chat_command_functions import add_cooldown
    add_cooldown(account_id, 'info', 10.0)  # Добавляем кулдаун для команды
    if 'page' in command_keys:
        page = command_keys['page']  # Получаем номер страницы из ключей команды
    else:
        page = 1  # Если ключей нет, устанавливаем страницу по умолчанию
    show_info(client_id, type, page)  # Вызываем функцию для отображения информации

# Функция для отображения информации
def show_info(client_id, type, page):
    type = 3  # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()  # Получаем текущую сессию
    from ModData.account_info import client_to_account, client_to_display_string
    account_id = client_to_account(client_id)  # Получаем ID аккаунта клиента
    account_name = client_to_display_string(client_id)  # Получаем имя аккаунта клиента

    from ModData.me import get_role
    role = get_role(account_id, account_name, client_id)  # Получаем роль пользователя

    from chatCommands.execute_command import check_permission
    from chatCommands.Commands import Creator, Admins, Players
    commands_list = []
    commands_list_show = []
    for command_module in [Creator, Admins, Players]:
        for command_name in command_module.__all__:
            command_submodule = getattr(command_module, command_name)
            if check_permission(client_id, account_id, account_name, command_name, command_module) and command_name not in commands_list:
                commands_list.append(command_name)  # Добавляем команду в список команд
                command_str = command_name
                if hasattr(command_submodule, 'aliases') and len(command_submodule.aliases) > 0:
                    aliases_str = ''
                    for alias in command_submodule.aliases:
                        if aliases_str != '':
                            aliases_str += ', '
                        aliases_str += alias
                    command_str += ', ' + aliases_str  # Добавляем алиасы к строке команды
                if hasattr(command_submodule, 'description'):
                    command_str += '    -    ' + command_submodule.description  # Добавляем описание к строке команды
                commands_list_show.append(command_str)  # Добавляем команду в список для отображения
    commands_list_show.sort()  # Сортируем список команд
    from chatCommands.chat_command_functions import show_pages
    showmessage(client_id, type, '========== доступные команды: ==========', _white_)
    show_pages(client_id, commands_list_show, type, page)  # Отображаем команды по страницам
