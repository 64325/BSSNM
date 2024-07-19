import random

import ba, _ba

description = 'попросить размут'  # Описание команды

invisible_command = True

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys):
    ask_for_unmute(client_id, account_id, type)  # Вызов функции для запроса на размут

# Функция для запроса на размут
def ask_for_unmute(client_id, account_id, type):
    type = 1  # вывод только в чат
    from chatHandle.chat_functions import showmessage, _red_, _light_yellow_
    from chatCommands.chat_command_functions import add_cooldown
    from ModData.account_info import client_to_player
    session = _ba.get_foreground_host_session()
    if account_id in session.playersData['mutelist']:
        add_cooldown(account_id, 'unmute', 600.0)  # Добавление кулдауна на команду
        player_name = client_to_player(client_id)  # Получение имени игрока
        showmessage(-1, 2, 'игрок ' + player_name + ' просит размут', _light_yellow_)  # Отправка сообщения всем
    else:
        showmessage(client_id, 2, 'вы не в муте', _red_)  # Отправка сообщения игроку, если он не в муте
