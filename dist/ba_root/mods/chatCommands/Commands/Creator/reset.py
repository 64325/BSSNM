import time

import ba, _ba

# Описание команды и её использование
description = 'сбросить статистику и начать новый сезон'

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    return True

# Функция для выполнения команды сброса статистики
def run_command(client_id, account_id, type, command_keys):
    reset_stats(client_id, account_id, type)

# Функция для сброса статистики и начала нового сезона
def reset_stats(client_id, account_id, type):
    from chatHandle.chat_functions import showmessage, _light_yellow_
    from ModData import stats
    
    # Получение текущей сессии и обновление статистики
    session = _ba.get_foreground_host_session()
    session.update_stats()
    
    # Логирование команды сброса статистики
    from chatCommands.chat_command_functions import log_command
    log_command(account_id, 'reset', None)
    
    # Сброс статистики
    stats.reset_stats()
    session.update_stats()
    
    # Обновление данных сервера
    from ModData import server_data as sd
    server_data = sd.load_server_data()
    
    # Увеличение номера сезона или установка его в 1, если нет данных о сезоне
    if 'season' in server_data:
        server_data['season'] += 1
    else:
        server_data['season'] = 1
    
    # Установка даты следующего сброса топовых данных через 30 дней
    server_data['top reset date'] = time.ctime(time.time() + 30.0 * 24.0 * 60.0 * 60.0)
    
    # Сохранение обновлённых данных сервера
    sd.save_server_data(server_data)
    session.load_server_data()
    
    # Вывод сообщения о сбросе статистики в чат
    showmessage(-1, 2, 'статистика сброшена', _light_yellow_)
