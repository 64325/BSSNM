import ba, _ba

description = 'изменить размер лобби'
info = [
    '                              изменить размер лобби',
    '                                        /mp   число',
    '                         изменить макс. число игроков',
    '                                  /mp players   число'
]

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'players' in command['args']:
        command['args'].remove('players')
        command['parsed_keys']['type'] = 'players'
    else:
        command['parsed_keys']['type'] = 'lobby'
    if len(command['args']) == 0:
        showmessage(-1, command['type'], 'введите число', _red_)
        return False
    try:
        value = int(command['args'][0])
        command['args'].pop(0)
    except:
        return False
    value = min(100, max(1, value))
    command['parsed_keys']['value'] = value
    return True

def run_command(client_id, account_id, type, command_keys):
    set_maxplayers(client_id, command_keys['type'], command_keys['value'])

def set_maxplayers(client_id, type, value):
    from chatHandle.chat_functions import showmessage, _light_yellow_
    session = _ba.get_foreground_host_session()
    if type == 'players':
        session.max_players = value
        showmessage(-1, 2, 'текущее макс. число игроков: ' + str(value), _light_yellow_)
    else:
        _ba.set_public_party_max_size(value + 1)
        session.max_players = value
        showmessage(-1, 2, 'текущий размер лобби: ' + str(value), _light_yellow_)