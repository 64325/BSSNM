import time

import ba, _ba

# Описание команды
description = 'обновить данные сессии'

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    return True

# Функция для выполнения команды обновления данных сессии
def run_command(client_id, account_id, type, command_keys):
    update_data(client_id, type)

# Функция для обновления данных сессии
def update_data(client_id, type):
    from chatHandle.chat_functions import showmessage, _light_yellow_
    
    # Получение текущей сессии
    session = _ba.get_foreground_host_session()
    
    # Обновление счётчика ошибок обновления статистики
    session.update_stats_fails = 0
    
    # Обновление различных данных сессии
    session.update_stats()
    session.update_banlist()
    session.update_mutelist()
    session.update_warnlist()
    session.update_effects()
    session.update_allow_data()
    session.update_roles()
    
    # Загрузка данных сервера
    session.load_server_data()
    
    # Получение текущей активности в игре
    activity = ba.getactivity()
    
    # Обновление информации на экране активности, если есть связанные сезонные данные
    if hasattr(activity, 'on_screen_text') and 'toplist' in activity.on_screen_text:
        if activity.on_screen_text['season_name']:
            activity.on_screen_text['season_name'].delete()
        if activity.on_screen_text['update_info']:
            activity.on_screen_text['update_info'].delete()
        if activity.on_screen_text['toplist']:
            activity.on_screen_text['toplist'].delete()
        activity.show_server_top()
    
    # Вывод сообщения о завершении обновления данных сессии
    showmessage(-1, 2, 'данные сессии обновлены', _light_yellow_)
