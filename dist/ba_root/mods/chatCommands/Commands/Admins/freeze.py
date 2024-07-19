import ba, _ba

aliases = ['fr']
description = 'заморозить игрока'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    freeze(player)

def freeze(cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if not player.actor.node.frozen:
                    player.actor.frozen = True
                    player.actor.node.frozen = True
                    ba.timer(10.0, ba.WeakCall(player.actor.handlemessage,
                                      ba.ThawMessage()))
                else:
                    player.actor.frozen = False
                    player.actor.node.frozen = False