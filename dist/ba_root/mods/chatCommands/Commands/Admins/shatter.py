import ba, _ba

aliases = ['sh']
description = 'разорвать игрока на части'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    shatter(player)

def shatter(cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if not player.actor.node.shattered:
                    player.actor.shattered = True
                    player.actor.node.shattered = 1
                else:
                    player.actor.shattered = False
                    player.actor.node.shattered = 0