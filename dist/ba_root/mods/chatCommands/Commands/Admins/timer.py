import time

import ba, _ba

description = 'включить таймер'


def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if len(command['args']) == 1 and 'del' in command['args']:
        command['parsed_keys']['action'] = 'delete'
        command['args'].remove('del')
        return True
    if 't' not in command['keys']:
        showmessage(client_id, command['type'], 'укажите интервал таймера', _red_)
        return False
    try:
        if len(command['keys']['t']) != 1:
            return False
        command['timer_interval'] = min(1000.0, max(0.01, float(command['keys']['t'][0])))
        command['keys'].pop('t')
    except:
        return False
    if 'repeat' in command['args']:
        command['args'].remove('repeat')
        command['repeat'] = True
        if 'o' in command['keys']:
            try:
                offset = min(1000.0, max(0.0, float(command['keys']['o'][0]))) % command['timer_interval']
                command['keys'].pop('o')
                command['timer_offset'] = offset
            except:
                return False
    else:
        command['is_delayed'] = True
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите название команды', _red_)
        return False
    command['name'] = command['args'][0]
    command['args'].pop(0)
    return True

def run_command(client_id, account_id, type, command_keys):
    if 'action' in command_keys and command_keys['action'] == 'delete':
        delete_timers()
    else:
        print('ошибка в команде timer')

def delete_timers():
    from chatHandle.chat_functions import showmessage, _light_yellow_
    session = _ba.get_foreground_host_session()
    session.commandsTimers = []
    showmessage(-1, 2, 'таймеры удалены', _light_yellow_)
        