import os

import ba, _ba

description = 'отправить личное сообщение'  # Описание команды
info = [
    '                       отправить личное сообщение',
    '                     /pm   номер игрока   сообщение'
]

invisible_command = True
using_players_ids = True
using_string_arg = True

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys, player):
    from chatCommands.chat_command_functions import add_cooldown
    add_cooldown(account_id, 'pm', 5.0)  # Добавление кулдауна на команду
    if player != client_id and command_keys['string_arg'] != '':
        send_private_message(client_id, player, command_keys['string_arg'])  # Вызов функции для отправки личного сообщения

# Функция для отправки личного сообщения
def send_private_message(client_id, cl_id, msg):
    from chatHandle.chat_functions import showmessage, _white_
    from ModData.account_info import client_to_account, client_to_display_string, client_to_player
    account_name = client_to_player(client_id)  # Получение имени игрока
    color = _white_
    session = _ba.get_foreground_host_session()  # Получение текущей игровой сессии
    try:
        for player in session.sessionplayers:  # Перебор всех игроков в сессии
            if player.inputdevice.client_id == client_id:
                color = (max(0.1, player.color[0]), max(0.1, player.color[1]), max(0.1, player.color[2]))  # Получение цвета игрока
    except:
        pass
    showmessage(client_id, 3, ' ' + msg, sender=ba.charstr(ba.SpecialChar.DICE_BUTTON2) + '[' + account_name + ']')  # Отправка сообщения себе
    showmessage(cl_id, 3, ' ' + msg, sender=ba.charstr(ba.SpecialChar.DICE_BUTTON2) + '[' + account_name + ']')  # Отправка сообщения другому игроку
