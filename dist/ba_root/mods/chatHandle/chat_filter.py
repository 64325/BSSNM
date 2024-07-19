from __future__ import annotations

from typing import TYPE_CHECKING

import os

import _ba, ba
import time

from ModData.account_info import client_to_account, client_to_display_string, client_to_player
from ModData.strings import *
from chatHandle.chat_functions import showmessage
from chatCommands.chat_command import is_command, handle_chat_command

# Путь для сохранения журнала чата
data_path = os.path.join(_ba.env()['python_directory_user'], "chatHandle", "chatLog" + os.sep)

# Цвета для форматирования сообщений
_red_ = (1.0, 0.1, 0.0)
_white_ = (1.0, 1.0, 1.0)

# Если используется статическая проверка типов (type checking)
if TYPE_CHECKING:
    from typing import Sequence, Optional, Any
    import ba

# Фильтрация чат-сообщений
def filter_chat_message(msg: str, client_id: int) -> str | None:
    # Получаем текущую сессию
    session = _ba.get_foreground_host_session()
    
    # Проверяем наличие необходимых атрибутов в сессии
    if not hasattr(session, 'playersData') or not hasattr(session, 'localPlayersData'):
        return None
    
    # Если клиент не принят в игру, игнорируем сообщение
    if client_id != -1 and client_id not in session.localPlayersData['accepted_clients']:
        return None

    # Получаем идентификатор аккаунта клиента
    account_id = client_to_account(client_id)
    if account_id == '':
        return None
    
    # Получаем отображаемое имя аккаунта
    account_name = client_to_display_string(client_id)
    if account_name == '':
        return None
    
    # Получаем имя игрока
    player_name = client_to_player(client_id)

    # Если клиент не анонимный
    if client_id != -1:
        # Проверяем нахождение аккаунта в мут-листе
        if account_id in session.localPlayersData['mutelist']:
            return None
        
        # Записываем время последнего сообщения
        cur_time = time.time()
        if account_id not in session.localPlayersData['chat_entries']:
            session.localPlayersData['chat_entries'][account_id] = []
        session.localPlayersData['chat_entries'][account_id].append(cur_time)
        
        # Удаляем старые записи из списка сообщений
        while len(session.localPlayersData['chat_entries'][account_id]) != 0:
            if session.localPlayersData['chat_entries'][account_id][0] < cur_time - 2.0:
                session.localPlayersData['chat_entries'][account_id].pop(0)
            else:
                break
        
        # Если сообщений слишком много, добавляем аккаунт в мут-лист
        if len(session.localPlayersData['chat_entries'][account_id]) >= 8:
            session.localPlayersData['mutelist'][account_id] = {}

    # Если клиент не анонимный
    if client_id != -1:
        # Проверяем наличие аккаунта или имени в мут-листе и записываем сообщение в журнал
        if (account_id in session.playersData['mutelist']
                or account_name in session.playersData['mutelist']):
            chat_log(client_id, msg + '   [muted]')
        else:
            chat_log(client_id, msg)

    # Если сообщение не является командой
    if not is_command(msg, client_id, account_id, account_name):
        # Проверяем наличие аккаунта или имени в мут-листе и возвращаем сообщение
        if account_id in session.playersData['mutelist'] or account_name in session.playersData['mutelist']:
            showmessage(client_id, 2, muted_str, _red_)
            return None
        else:
            return msg
    else:
        # Если сообщение является командой, обрабатываем её
        if handle_chat_command(msg, client_id, account_id, account_name):
            return msg if client_id != -1 else msg[1:]
        else:
            return None

# Запись сообщения в журнал чата
def chat_log(client_id, msg):
    # Импортируем функцию для форматирования времени
    from chatHandle.chat_functions import translate_time
    
    # Создаем строку для записи в журнал
    logstr = translate_time(time.ctime(time.time()))
    
    # Получаем идентификатор аккаунта, отображаемое имя и имя игрока
    account_id = client_to_account(client_id)
    display_string = client_to_display_string(client_id)
    player_name = client_to_player(client_id)
    
    # Добавляем информацию в строку
    if account_id != '':
        logstr += ' | ' + str(account_id)
    if display_string != '':
        logstr += ' | ' + display_string
    if player_name != '':
        logstr += ' | ' + player_name
    
    # Добавляем сообщение
    logstr += ' > ' + msg
    
    # Формируем имя файла для журнала чата
    filename = data_path + _ba.app.server._config.party_name + ".log"
    
    # Если файл уже существует, добавляем в него запись
    if os.path.exists(filename):
        with open(filename, "a") as file:
            file.write('\n' + logstr)
    else:
        # Иначе создаем новый файл и записываем в него
        with open(filename, "w") as file:
            file.write(logstr)
