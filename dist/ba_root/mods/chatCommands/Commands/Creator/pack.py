import random

import ba, _ba

# Описание команды и информация о её использовании
description = 'работа с пакетами'
info = [
    '                     создать пакет с одной командой',
    '                          /pack   название   команда',
    '                          добавить команду в пакет',
    '                  /pack add   название   новая команда',
    '                                  скопировать пакет',
    '                  /pack   новый пакет   &старый пакет',
    '                       стереть последнюю команду',
    '                               /pack pop   название',
    '                                    удалить пакет',
    '                                /pack del   название',
    '                                   список пакетов',
    '                                         /pack list',
    '     Не используйте команду pack для запуска пакета!',
    '                                   запустить пакет',
    '                /&название пакета   доп.параметры'
]

# Функция для извлечения аргументов из команды
def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    
    # Обработка аргумента 'list' или 'l' для вывода списка пакетов
    if 'list' in command['args']:
        command['args'].remove('list')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            try:
                value = int(command['args'][0])
                command['args'].pop(0)
            except:
                return False
            command['parsed_keys']['page'] = max(0, value)
        return True
    elif 'l' in command['args']:
        command['args'].remove('l')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            try:
                value = int(command['args'][0])
                command['args'].pop(0)
            except:
                return False
            command['parsed_keys']['page'] = max(0, value)
        return True
    elif 'show' in command['args']:
        command['args'].remove('show')
        command['parsed_keys']['action'] = 'show_packet'
    elif 'add' in command['args']:
        command['args'].remove('add')
        command['parsed_keys']['action'] = 'add'
    elif 'pop' in command['args']:
        command['args'].remove('pop')
        command['parsed_keys']['action'] = 'pop'
    elif 'del' in command['args']:
        command['args'].remove('del')
        command['parsed_keys']['action'] = 'delete'
    else:
        command['parsed_keys']['action'] = 'set'
    
    # Проверка на наличие имени пакета в аргументах
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите имя пакета', _red_)
        return False
    
    package_name = command['args'][0]
    command['args'].pop(0)
    
    from chatHandle.chat_functions import string_type
    
    # Проверка на допустимость имени пакета
    if string_type(package_name) != 'name':
        showmessage(client_id, command['type'], 'недопустимое имя пакета', _red_)
        return False
    
    command['parsed_keys']['package_name'] = package_name
    command['parsed_keys']['strings'] = []
    
    # Если действие 'add', добавляем строку для создания пакета
    if command['parsed_keys']['action'] == 'add':
        command['parsed_keys']['action'] = 'set'
        command['parsed_keys']['strings'].append('&' + package_name)
    elif command['parsed_keys']['action'] == 'show_packet' or command['parsed_keys']['action'] == 'pop' or command['parsed_keys']['action'] == 'delete':
        return True
    
    # Извлечение оставшихся строк в аргументах как команды для пакета
    while len(command['args']) > 0:
        command['parsed_keys']['strings'].append(command['args'][0])
        command['args'].pop(0)
    
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys):
    from chatHandle.chat_functions import showmessage, _red_
    session = _ba.get_foreground_host_session()
    session.load_server_data()
    
    # Проверка на наличие списка пакетов в серверных данных
    if 'packages' not in session.serverData:
        showmessage(client_id, type, 'список пакетов недоступен', _red_)
        return
    
    # Обработка действий в зависимости от ключа 'action' из команды
    if command_keys['action'] == 'show':
        if 'page' in command_keys:
            page = command_keys['page']
        else:
            page = 1
        show_packages(client_id, type, page)
        return
    
    package_name = command_keys['package_name']
    
    if command_keys['action'] == 'show_packet':
        # Показать содержимое конкретного пакета
        if package_name not in session.serverData['packages']:
            showmessage(client_id, type, package_name + ': пакет не найден', _red_)
            return
        show_package(client_id, type, package_name)
        return
    
    if command_keys['action'] == 'set':
        # Добавить или обновить пакет
        add_package(client_id, account_id, type, package_name, command_keys['strings'])
        return
    
    # Удаление последней команды из пакета
    if package_name not in session.serverData['packages']:
        showmessage(client_id, type, package_name + ': пакет не найден', _red_)
        return
    
    if command_keys['action'] == 'pop':
        pop_package(client_id, type, package_name)
        return
    
    # Удаление пакета
    if command_keys['action'] == 'delete':
        remove_package(client_id, type, package_name)
        return

# Функция для добавления пакета с командами
def add_package(client_id, account_id, type, package_name, strings):
    from chatHandle.chat_functions import showmessage, _red_, _white_
    session = _ba.get_foreground_host_session()
    
    # Проверка наличия команд в пакете
    if len(strings) == 0:
        showmessage(client_id, type, 'добавьте команды в пакет', _red_)
        return
    
    from chatHandle.chat_functions import string_type
    
    package_lines = []
    current_line = ''
    
    # Обработка каждой строки команды
    while len(strings) > 0:
        word = strings[0]
        strings.pop(0)
        
        # Удаление кавычек и разделение по ;
        if len(word) >= 2 and word[0] == "'" and word[-1] == "'":
            word = word[1:-1]
        
        if ';' in word and word != ';':
            word_split = word.split(';')
            word = ';'
            add_words = []
            while len(word_split) > 0:
                add_words.append(word_split[0])
                word_split.pop(0)
                add_words.append(';')
            strings = add_words + strings
        
        while word.startswith(' '):
            word = word[1:]
        
        while word.endswith(' '):
            word = word[:-1]
        
        if len(word) != 0:
            if string_type(word) == 'package':
                # Добавление команд из другого пакета
                add_package_name = word[1:]
                if add_package_name not in session.serverData['packages']:
                    showmessage(client_id, type, add_package_name + ': пакет не найден', _red_)
                    return
                if current_line != '':
                    package_lines.append(current_line)
                    current_line = ''
                for line in session.serverData['packages'][add_package_name]['commands']:
                    package_lines.append(line)
                if current_line != '':
                    package_lines.append(current_line)
                    current_line = ''
            elif word == ';':
                # Обработка разделителя ;
                if current_line != '':
                    package_lines.append(current_line)
                    current_line = ''
            else:
                # Добавление обычной команды в текущую строку
                if current_line != '' and word != ',':
                    current_line += ' '
                current_line += word
    
    # Добавление последней строки, если она не пуста
    if current_line != '':
        package_lines.append(current_line)
        current_line = ''
    
    # Получение имени аккаунта
    from ModData.account_info import client_to_display_string
    account_name = client_to_display_string(client_id)
    
    package = {
        'account id': account_id
    }
    
    # Добавление имени аккаунта в пакет, если оно есть
    if account_name != '':
        package['account name'] = account_name
    
    # Сохранение команд в пакете
    if len(package_lines) != 0:
        package['commands'] = package_lines
        session.serverData['packages'][package_name] = package
        from ModData import server_data as sd
        sd.save_packages(session.serverData['packages'])
        showmessage(client_id, type, 'пакет ' + package_name + ' обновлён', _white_)

# Функция для удаления последней команды из пакета
def pop_package(client_id, type, package_name):
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    session.serverData['packages'][package_name]['commands'].pop(-1)
    
    # Проверка на пустоту пакета после удаления
    if len(session.serverData['packages'][package_name]['commands']) == 0:
        session.serverData['packages'].pop(package_name)
        showmessage(client_id, type, 'пакет ' + package_name + ' удалён', _white_)
    else:
        showmessage(client_id, type, 'пакет ' + package_name + ' обновлён', _white_)
    
    # Сохранение обновлённого списка пакетов
    from ModData import server_data as sd
    sd.save_packages(session.serverData['packages'])

# Функция для удаления пакета целиком
def remove_package(client_id, type, package_name):
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    session.serverData['packages'].pop(package_name)
    showmessage(client_id, type, 'пакет ' + package_name + ' удалён', _white_)
    
    # Сохранение обновлённого списка пакетов
    from ModData import server_data as sd
    sd.save_packages(session.serverData['packages'])

# Функция для вывода списка всех пакетов
def show_packages(client_id, type, page):
    if type == 2:
        type = 3 # вывод только в чат
    
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    
    # Вывод заголовка списка пакетов
    showmessage(client_id, type, '=============== пакеты: ===============', _white_)
    packages_list_show = []
    
    # Формирование списка пакетов для вывода
    for package_name in session.serverData['packages']:
        package_str = package_name
        
        # Добавление имени создателя пакета
        if 'account name' in session.serverData['packages'][package_name] and session.serverData['packages'][package_name]['account name'] != '':
            package_str += '  by  ' + session.serverData['packages'][package_name]['account name']
        elif 'account id' in session.serverData['packages'][package_name]:
            package_str += '  by  ' + session.serverData['packages'][package_name]['account id']
        
        packages_list_show.append(package_str)
    
    # Вывод списка пакетов с разбивкой по страницам
    from chatCommands.chat_command_functions import show_pages
    show_pages(client_id, packages_list_show, type, page)

# Функция для вывода содержимого конкретного пакета
def show_package(client_id, type, package_name):
    if type == 2:
        type = 3 # вывод только в чат
    
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    
    # Вывод заголовка пакета
    showmessage(client_id, type, '========= пакет ' + package_name + ': =========', _white_)
    
    # Вывод содержимого команд в пакете
    for line in session.serverData['packages'][package_name]['commands']:
        showmessage(client_id, type, '    ' + line, _white_)
