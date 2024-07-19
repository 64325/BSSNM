from __future__ import annotations  # Используем новый синтаксис для аннотаций типов

from typing import TYPE_CHECKING

import os

import _ba, ba  # Импортируем необходимые модули
import time

from ModData.account_info import client_to_account, client_to_display_string, client_to_player  # Импортируем функции и данные из различных модулей
from ModData.strings import *
from chatHandle.chat_functions import string_type, showmessage
from chatCommands.execute_command import normalise_command_name, check_permission, execute

from .Commands import Creator, Admins, Players  # Импортируем команды из различных модулей

_red_ = (1.0, 0.1, 0.0)  # Определяем цвета для сообщений
_white_ = (1.0, 1.0, 1.0)

def is_command(msg, client_id, account_id, account_name):
    if msg == '/unmute':  # Проверяем, является ли сообщение командой /unmute
        return True
    session = _ba.get_foreground_host_session()  # Получаем текущую сессию
    if account_id in session.playersData['mutelist'] or account_name in session.playersData['mutelist']:  # Проверяем, замучен ли игрок
        return False
    if client_id == -1:  # Если клиент не определён
        if msg.startswith('$'):  # Проверяем начинается ли сообщение с $
            msg_start = msg[1:].split(';')[0].split(' ')[0]
            if string_type(msg_start) == 'name' or string_type(msg_start) == 'package':  # Проверяем тип строки
                return True
    elif msg.startswith('/') or msg.startswith(':'):  # Если сообщение начинается с / или :
        msg_start = msg[1:].split(';')[0].split(' ')[0]
        if string_type(msg_start) == 'name' or string_type(msg_start) == 'package':  # Проверяем тип строки
            return True
    return False

def get_command_type_and_string(msg, client_id, account_id):
    if msg[0] == '/':  # Если сообщение начинается с /
        return 1, msg[1:]  # Возвращаем тип команды и саму команду
    elif msg[0] == ':':  # Если сообщение начинается с :
        return 2, msg[1:]  # Возвращаем тип команды и саму команду
    elif msg[0] == '$':  # Если сообщение начинается с $
        return 1, msg[1:]  # Возвращаем тип команды и саму команду

def handle_chat_command(msg, client_id, account_id, account_name):
    command_type, msg = get_command_type_and_string(msg, client_id, account_id)  # Получаем тип команды и саму команду
    send_msg_to_chat = command_type == 1  # Определяем, нужно ли отправлять сообщение в чат
    commands = parse_commands(msg)  # Парсим команды из сообщения
    for command in commands:
        command['type'] = command_type  # Устанавливаем тип команды
        command_modules = get_command_modules(command['name'])  # Получаем модули команды
        if len(command_modules) == 0:  # Если модули не найдены
            from ModData.me import get_role, get_value
            if get_value(get_role(account_id, account_name, client_id)) > 0:  # Проверяем права пользователя
                showmessage(client_id, command_type, command['name'] + ': ' + command_not_found_str, _red_)  # Отправляем сообщение о том, что команда не найдена
        else:
            chosen_module = None
            for command_module in command_modules:
                if command['permitted'] == True or check_permission(client_id, account_id, account_name, command['name'], command_module):
                    chosen_module = command_module  # Выбираем модуль для выполнения команды
            if chosen_module == None:  # Если модуль не выбран
                from ModData.me import get_value, get_role
                if Players in command_modules or get_value(get_role(account_id, account_name, client_id)) > 0:
                    showmessage(client_id, command_type, command['name'] + ': ' + permission_denied_str, _red_)  # Отправляем сообщение о том, что доступ запрещён
            else:
                normalise_command_name(client_id, account_id, command, chosen_module)  # Нормализуем имя команды
                if hasattr(getattr(chosen_module, command['name']), 'invisible_command') and getattr(chosen_module, command['name']).invisible_command:
                    send_msg_to_chat = False  # Если команда невидима, не отправляем сообщение в чат
                execute_result = execute(client_id, account_id, account_name, command, chosen_module)  # Выполняем команду
                if execute_result == 'change':  # Если требуется изменение
                    commands.append(command)  # Добавляем команду

    return send_msg_to_chat  # Возвращаем флаг отправки сообщения в чат

def parse_command_string(msg):

    # делим на отдельные команды
    quotes_open = False
    msg_parts = []
    current_part = ''
    for c in msg:
        if c == "'":
            quotes_open = not quotes_open
        if c == ';' and not quotes_open:
            msg_parts.append(current_part)
            current_part = ''
        else:
            current_part += c
    msg_parts.append(current_part)
    while '' in msg_parts:
        msg_parts.remove('')

    # делим команды на слова
    quotes_open = False
    commands_words = []
    for part in msg_parts:
        phrase = []
        current_word = ''
        for c in part:
            if c == "'":
                if not quotes_open:
                    phrase.append(current_word)
                    current_word = ''
                    current_word += c
                else:
                    current_word += c
                    phrase.append(current_word)
                    current_word = ''
                quotes_open = not quotes_open
            elif c == ' ' and not quotes_open:
                phrase.append(current_word)
                current_word = ''
            elif c == '=' and not quotes_open:
                if string_type(current_word + c) == 'pb_id':
                    current_word += c
                else:
                    phrase.append(current_word)
                    phrase.append(c)
                    current_word = ''
            elif c == ',' and not quotes_open:
                phrase.append(current_word)
                phrase.append(c)
                current_word = ''
            else:
                current_word += c
        if quotes_open:
            current_word += "'"
        phrase.append(current_word)
        while '' in phrase:
            phrase.remove('')
        if len(phrase) != 0:
            commands_words.append(phrase)
    return commands_words

def parse_commands(msg):

    session = _ba.get_foreground_host_session()
    server_data = session.serverData

    commands_words = parse_command_string(msg)

    # муторная обработка пакетов
    commands_words_final = []
    for phrase in commands_words:
        if phrase[0] == 'pack':
            commands_words_final.append(phrase)
        else:
            packages_in_phrase = 0
            package_word = ''
            for word in phrase:
                if string_type(word) == 'package':
                    packages_in_phrase += 1
                    package_word = word
            if packages_in_phrase == 0 or phrase[0] in ['pm', 'wm', 'tm']:
                commands_words_final.append(phrase)
            elif packages_in_phrase == 1:
                package_index = phrase.index(package_word)
                package_name = package_word[1:]
                if 'packages' in server_data and package_name in server_data['packages']:
                    for line in server_data['packages'][package_name]['commands']:
                        package_words = parse_command_string(line)[0]
                        commands_words_final.append(phrase[:package_index] + package_words + phrase[package_index + 1:])
                else:
                    showmessage(-1, 1, package_name + ': ' + package_not_found_str, _red_)
                    return []
            else:
                showmessage(-1, 1, more_then_1_package_in_command_str, _red_)
                return []

    # собираем команды
    commands = []
    for phrase in commands_words_final:
        command = {
            'args': [],
            'keys': {}
        }
        if len(phrase) >= 1 and phrase[0] in ['pack', 'pm', 'wm', 'tm']:
            while len(phrase) > 0:
                s = phrase[0]
                phrase.pop(0)
                command['args'].append(s)
        else:
            while len(phrase) > 0:
                s = phrase[0]
                phrase.pop(0)
                if len(phrase) >= 2 and phrase[0] == '=':
                    phrase.pop(0)
                    if string_type(s) != 'name':
                        showmessage(-1, 1, command_string_error_str, _red_)
                        return []
                    command['keys'][s] = [phrase[0]]
                    phrase.pop(0)
                    while len(phrase) >= 2 and phrase[0] == ',':
                        phrase.pop(0)
                        #if string_type(phrase[0]) != 'name':
                        #    showmessage(-1, 1, command_string_error_str, _red_)
                        #    return []
                        command['keys'][s].append(phrase[0])
                        phrase.pop(0)
                elif s == ',':
                    showmessage(-1, 1, command_string_error_str, _red_)
                    return []
                else:
                    command['args'].append(s)
        if len(command['args']) == 0:
            showmessage(-1, 1, command_string_error_str, _red_)
            return []
        command['name'] = command['args'][0]
        command['permitted'] = None
        command['args'].pop(0)
        if string_type(command['name']) != 'name':
            showmessage(-1, 1, command_string_error_str, _red_)
            return []
        commands.append(command)
    return commands

def get_command_modules(command_name):
    session = _ba.get_foreground_host_session()
    server_data = session.serverData

    modules = []
    for command_module in [Players, Admins, Creator]:
        if hasattr(command_module, command_name):
            modules.append(command_module)
        else:
            for name in command_module.__all__:
                if hasattr(command_module, name):
                    command_submodule = getattr(command_module, name)
                    if hasattr(command_submodule, 'aliases') and command_name in command_submodule.aliases:
                        modules.append(command_module)
                        break
    return modules
