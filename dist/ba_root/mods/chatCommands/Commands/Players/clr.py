import random

import ba, _ba

description = 'посмотреть цвета и анимации'

def extract_args(client_id, account_id, command):
    # Функция для извлечения аргументов из команды
    return True

def run_command(client_id, account_id, type, command_keys):
    # Основная функция для выполнения команды
    from chatCommands.chat_command_functions import add_cooldown
    add_cooldown(account_id, 'clr', 10.0)
    show_colors(client_id, type)

def show_colors(client_id, type):
    # Функция для отображения цветов и анимаций
    type = 1 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    from ba._activity import actor_colors, actor_animations
    showmessage(client_id, type, '================ цвета: ================', _white_)
    color_str = ''
    i = 0
    for color in actor_colors:
        # Перебор всех цветов
        i += 1
        if color_str != '':
            color_str += '   '
        color_str += color
        if i != len(actor_colors):
            color_str += ','
        if i % 3 == 0 or i == len(actor_colors):
            # Показ цветов в чат
            showmessage(client_id, type, '    ' + color_str, _white_)
            color_str = ''
    showmessage(client_id, type, '=============== анимации: ===============', _white_)
    for animation in actor_animations:
        # Перебор всех анимаций
        showmessage(client_id, type, '    ' + animation, _white_)
