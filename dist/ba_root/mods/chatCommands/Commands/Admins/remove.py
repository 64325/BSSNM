import math

import ba, _ba

aliases = ['rm']
description = 'переместить в лобби'

using_players_ids = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    remove_player(player)

def remove_player(cl_id):
    session = _ba.get_foreground_host_session()
    for player in session.sessionplayers:
        if player.inputdevice.client_id == cl_id:
            player.remove_from_game()
            