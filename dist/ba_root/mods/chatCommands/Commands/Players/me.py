import os

import ba, _ba

aliases = ['stats']
description = 'показать статистику'

using_players_ids = True

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    if 'all' in command['args'] or 'a' in command['args'] or len(command['args']) > 1:
        return False
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys, player):
    from chatCommands.chat_command_functions import add_cooldown
    add_cooldown(account_id, 'me', 10.0)  # Добавление кулдауна на команду
    show_me_info(client_id, type, player)  # Вызов функции для отображения информации

# Функция для отображения информации о пользователе
def show_me_info(client_id, type, cl_id):
    if type == 2:
        type = 3  # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    from ModData.account_info import client_to_account, client_to_display_string
    acc_id = client_to_account(cl_id)  # Получение идентификатора аккаунта
    acc_name = client_to_display_string(cl_id)  # Получение отображаемого имени аккаунта
    session = _ba.get_foreground_host_session()
    from ModData import me
    me_info, me_names = me.get_me_info(cl_id, acc_id, acc_name)  # Получение информации о пользователе
    me_text = []
    me_text.append('____________________ Info ____________________')
    accounts_line = ''
    acc_names = me_info['account_names']  # Получение имен аккаунтов
    if len(acc_names) > 4:
        acc_names = acc_names[:4] + [' ...']
    for acc in acc_names:
        if acc != '':
            if accounts_line != '':
                accounts_line += '  ·  '
            accounts_line += acc
    if accounts_line != '':
        me_text.append(accounts_line)
    account_info_line = '  ' + str(cl_id) + '     ·     ' + (' ? ' if acc_id == '' else acc_id) + '                   ' + '<  ' + me_info['role'] + '  >'
    me_text.append(account_info_line)
    me_text.append('                  __________________________          ')
    me_names_line = ''
    me_values_line = ''
    for key in me_info:
        name = me_names[key]
        value = me_info[key]
        if key not in ['client_id', 'account_id', 'account_name', 'account_names', 'role']:
            if me_names_line != '':
                me_names_line += '    '
                me_values_line += '    '
            e1 = int(max(1, (len(name) - len(value)) / 2))
            e2 = int(max(1, (len(name) - len(value) + 1) / 2))
            value = '  ' * e1 + value + '  ' * e2
            if len(name) < 6:
                me_names_line += '  ' * (6 - len(name))
                me_values_line += '  ' * (6 - len(name))
            me_names_line += name
            me_values_line += value
            if len(name) < 6:
                me_names_line += '  ' * (6 - len(name))
                me_values_line += '  ' * (6 - len(name))
    me_text.append(me_names_line)
    me_text.append(me_values_line)
            

    for line in me_text:
        showmessage(client_id, type, line, _white_)  # Отображение сообщения в чате
