import os
import time

import ba, _ba

description = 'отправить ожидающее сообщение'  # Описание команды
info = [
    '                  отправить ожидающее сообщение',
    '            /wm   номер игрока или pb-id   сообщение'
]

invisible_command = True
using_players_ids = True
using_pb_ids = True
using_string_arg = True

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    if pb_id != account_id and command_keys['string_arg'] != '':
        send_waiting_message(client_id, pb_id, acc_name, command_keys['string_arg'])  # Вызов функции для отправки ожидающего сообщения

# Функция для отправки ожидающего сообщения
def send_waiting_message(client_id, pb_id, acc_name, msg):
    from chatHandle.chat_functions import showmessage, _red_, _white_
    from ModData.account_info import client_to_account, client_to_display_string, client_to_player
    account_name = client_to_display_string(client_id)  # Получение отображаемого имени аккаунта
    color = _white_
    session = _ba.get_foreground_host_session()
    try:
        for player in session.sessionplayers:
            if player.inputdevice.client_id == client_id:
                color = (max(0.1, player.color[0]), max(0.1, player.color[1]), max(0.1, player.color[2]))  # Получение цвета игрока
    except:
        pass
    from ModData import waiting_message as wm
    waiting_messages = wm.load_messages()  # Загрузка ожидающих сообщений
    if pb_id in waiting_messages and len(waiting_messages[pb_id]['messages']) >= 10:
        showmessage(client_id, 2, 'у игрока ' + pb_id + ' уже ' + str(len(waiting_messages[pb_id]['messages'])) + ' сообщений', _red_)  # Проверка, если у игрока уже есть 10 сообщений
        return
    wm.add_message(pb_id, acc_name, '[' + account_name + ']: ' + msg, color, time.time())  # Добавление сообщения в список ожидающих сообщений
    if acc_name == '':
        showmessage(client_id, 2, 'игрок ' + pb_id + ' получит ваше сообщение', _white_)  # Сообщение, если имя аккаунта пустое
    else:
        showmessage(client_id, 2, 'игрок ' + acc_name + ' получит ваше сообщение', _white_)  # Сообщение с именем аккаунта
    session.update_waiting_messages()  # Обновление ожидающих сообщений в сессии
