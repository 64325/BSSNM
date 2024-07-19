import ba, _ba

aliases = ['ri', 're']
description = 'возродить игрока'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    rise(player)

def rise(cl_id):
    activity = ba.getactivity()
    player_joined = False
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            player_joined = True
            if not player.actor or player.actor.node.dead:
                player.customdata['respawn_timer'] = None
                player.customdata['respawn_icon'] = None
                activity.spawn_player(player)
    if not player_joined:
        session = _ba.get_foreground_host_session()
        for player in session.sessionplayers:
            if player.inputdevice.client_id == cl_id:
                team = player.sessionteam
                activity.add_team(team)
                player.activityplayer = activity_player = activity.create_player(player)
                activity_player.postinit(player)
                team.activityteam.players.append(activity_player)
                activity.players.append(activity_player)
                activity_player.lives = 0
                if hasattr(activity_player.team, 'spawn_order'):
                    activity_player.team.spawn_order.append(activity_player)
                activity.spawn_player(activity_player)
                return