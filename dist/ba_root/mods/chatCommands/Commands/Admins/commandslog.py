import os

import ba, _ba

aliases = ['commands']
description = 'показать последние команды'
info = [
    '                               последние команды',
    '                             /commands   [страница]'
]

def extract_args(client_id, account_id, command):
    if len(command['args']) != 0:
        try:
            value = int(command['args'][0])
            command['args'].pop(0)
        except:
            return False
        command['parsed_keys']['page'] = max(0, value)
    return True

def run_command(client_id, account_id, type, command_keys):
    if 'page' in command_keys:
        page = command_keys['page']
    else:
        page = 1
    show_commandslog(client_id, type, page)

def show_commandslog(client_id, type, page):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    data_path = os.path.join(_ba.env()['python_directory_user'],"chatHandle", "commandsLog" + os.sep)
    filename = data_path + 'commands' + ".log"
    commands_log = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            commands_log = file.readlines()
    if len(commands_log) > 500:
        commands_log = commands_log[-500:]
    commands_log_show = []
    for line in commands_log:
        index = line.find(' > ')
        if index != -1:
            commands_log_show.append(line[:index])
            commands_log_show.append('    ' + line[index + 3:])
    commands_log_show.reverse() # страницы будут идти в обратном порядке!
    showmessage(client_id, type, '============ последние команды: ============', _white_)
    from chatCommands.chat_command_functions import show_pages
    show_pages(client_id, commands_log_show, type, page, long=True, inverse=True) # но на странице сообщения будут в обычном порядке, поэтому inverse
