import ba, _ba

description = 'радоваться'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    celeb(player)

def celeb(cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                player.actor.handlemessage(ba.CelebrateMessage(4.0))