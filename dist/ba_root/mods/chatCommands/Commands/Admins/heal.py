import ba, _ba

aliases = ['he']
description = 'вылечить игрока'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    heal(player)

def heal(cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                player.actor.hitpoints = player.actor.hitpoints_max
                player.actor.node.hurt = 0