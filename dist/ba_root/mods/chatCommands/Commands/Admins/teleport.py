import math

import ba, _ba

aliases = ['tp']
description = 'телепортировать игрока'
info = [
    '                     /teleport   x   y   z   номер игрока',
    '                                            или',
    '           /teleport   d=x,y,z(смещение)   номер игрока'
]

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    command['parsed_keys']['pos'] = []
    command['parsed_keys']['d'] = []
    if len(command['args']) >= 3:
        try:
            for i in range(3):
                value = float(command['args'][0])
                command['args'].pop(0)
                command['parsed_keys']['pos'].append(value)
        except:
            return False
    if 'd' in command['keys']:
        if len(command['keys']['d']) != 3:
            return False
        try:
            for i in range(3):
                value = float(command['keys']['d'][0])
                command['keys']['d'].pop(0)
                command['parsed_keys']['d'].append(value)
            command['keys'].pop('d')
        except:
            return False
    return True

def run_command(client_id, account_id, type, command_keys, player):
    teleport(player, command_keys['pos'], command_keys['d'])

def run_command_timer_on(client_id, account_id, type, command_keys, player):
    teleport_without_flash(player, command_keys['pos'], command_keys['d'])

def teleport(cl_id, pos, d):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if len(pos) == 0:
                    pos = player.actor.node.position_center
                if len(d) == 0:
                    d = [0.0, 0.0, 0.0]
                player.actor.node.handlemessage('stand', pos[0] + d[0], pos[1] + d[1] - 1.0, pos[2] + d[2], 0.0)
                explosion = ba.newnode('explosion',
                               attrs={
                                   'position': (pos[0] + d[0], pos[1] + d[1], pos[2] + d[2]),
                                   'velocity': (0.0, 0.0, 0.0),
                                   'big': False,
                                   'color': (0.05, 0.08, 0.4)
                               })
                ba.animate(explosion, 'radius', {0: 1.6, 0.5: 0.0})
                ba.timer(0.5, explosion.delete)

def teleport_without_flash(cl_id, pos, d):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if len(pos) == 0:
                    pos = player.actor.node.position_center
                if len(d) == 0:
                    d = [0.0, 0.0, 0.0]
                player.actor.node.handlemessage('stand', pos[0] + d[0], pos[1] + d[1] - 1.0, pos[2] + d[2], 0.0)
