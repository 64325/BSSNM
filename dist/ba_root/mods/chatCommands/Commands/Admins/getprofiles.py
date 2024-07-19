import ba, _ba

aliases = ['gp']
description = 'посмотреть профили игрока'

using_players_ids = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    get_profiles(client_id, type, player)

def get_profiles(client_id, type, cl_id):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    profilenames = []
    for player in session.sessionplayers:
        if player.inputdevice.client_id == cl_id:
            profiles = player.inputdevice.get_player_profiles()
            profilenames = list(profiles.keys())
            showmessage(client_id, type, '=============== профили: ===============', _white_)
            for profilename in profilenames:
                if profilename == '__account__':
                    showmessage(client_id, type, '    ' + player.getname(), _white_)
                else:
                    showmessage(client_id, type, '    ' + profilename, _white_)
            return
    showmessage(client_id, type, 'игрок не вошёл в игру', _white_)