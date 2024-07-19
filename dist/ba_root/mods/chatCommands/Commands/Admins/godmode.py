import ba, _ba

aliases = ['gm']
description = 'режим бога'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    set_godmode(player)

def set_godmode(cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if not hasattr(player.actor, 'godmode') or not player.actor.godmode:
                    player.actor.godmode = True
                    player.actor._protection()
                    if not player.actor.protection:
                        player.actor._protection()
                    player.actor.protection_light.node.color_texture = ba.gettexture('flagColor')
                    player.actor.protection_light.node.reflection_scale = (1.5, 1.5, 3.0)
                    player.actor._punch_cooldown = 100
                    player.actor._punch_power_scale = 1.2 * 2.5
                    player.actor.node.hockey = True
                    player.actor.speed = 3.0
                else:
                    player.actor.godmode = False
                    if player.actor.protection:
                        player.actor._protection()
                    player.actor._punch_cooldown = 400
                    player.actor._punch_power_scale = 1.2
                    player.actor.node.hockey = player.actor._hockey
                    player.actor.speed = 1.0
