import ba, _ba

aliases = ['pos']
description = 'позиция игрока'

using_players_ids = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    show_position(client_id, player, type)

def show_position(client_id, cl_id, type):
    if type == 2:
        type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    from ModData.account_info import client_to_player
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                x = round(player.actor.node.position_center[0], 1)
                y = round(player.actor.node.position_center[1], 1)
                z = round(player.actor.node.position_center[2], 1)
                showmessage(client_id, type, player.actor.node.name + ':   ' + str(x) + '  ' + str(y) + '  ' + str(z), _white_)
