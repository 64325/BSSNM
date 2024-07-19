import os

import ba, _ba

description = 'показать правила сервера'  # Описание команды

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    if len(command['args']) != 0:
        try:
            value = int(command['args'][0])
            command['args'].pop(0)  # Удаление первого аргумента из списка
        except:
            return False
        command['parsed_keys']['page'] = max(0, value)  # Сохранение страницы в команду
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys):
    if 'page' in command_keys:
        page = command_keys['page']
    else:
        page = 1
    show_rules(client_id, type, page)  # Вызов функции для отображения правил

# Функция для отображения правил
def show_rules(client_id, type, page):
    type = 3  # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    session.load_server_data()  # Загрузка данных сервера
    if 'rules' in session.serverData:
        from chatCommands.chat_command_functions import show_pages
        showmessage(client_id, type, '============= правила сервера: =============', _white_)  # Отправка сообщения с заголовком правил
        show_pages(client_id, session.serverData['rules'], type, page)  # Отображение правил по страницам
    else:
        showmessage(client_id, type, 'правил пока нет', _white_)  # Сообщение, если правил нет
