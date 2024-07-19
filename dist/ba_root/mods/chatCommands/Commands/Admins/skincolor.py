import math

import ba, _ba

description = 'изменить цвет персонажа'

using_players_ids = True
timer_compatible = True
info = [
    '/skincolor   clr1=цвет1',
    '/skincolor   clr2=цвет2'
]

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if len(command['keys']) == 0:
        showmessage(client_id, command['type'], 'укажите clr1 или clr2', _red_)
        return False
    command['parsed_keys']['color'] = []
    command['parsed_keys']['highlight'] = []
    from ba._activity import actor_colors, actor_animations
    if 'clr1' in command['keys']:
        if len(command['keys']['clr1']) == 1:
            color = command['keys']['clr1'][0]
            command['keys'].pop('clr1')
            if color not in actor_colors and color not in actor_animations:
                showmessage(client_id, command['type'], color + ': цвет не найден', _red_)
                return False
            command['parsed_keys']['color'].append(color)
        elif len(command['keys']['clr1']) == 3:
            try:
                for i in range(3):
                    value = float(command['keys']['clr1'][0])
                    command['keys']['clr1'].pop(0)
                    command['parsed_keys']['color'].append(value)
                command['keys'].pop('clr1')
            except:
                return False
    if 'clr2' in command['keys']:
        if len(command['keys']['clr2']) == 1:
            highlight = command['keys']['clr2'][0]
            command['keys'].pop('clr2')
            if highlight not in actor_colors and highlight not in actor_animations:
                showmessage(client_id, command['type'], highlight + ': цвет не найден', _red_)
                return False
            command['parsed_keys']['highlight'].append(highlight)
        elif len(command['keys']['clr2']) == 3:
            try:
                for i in range(3):
                    value = float(command['keys']['clr2'][0])
                    command['keys']['clr2'].pop(0)
                    command['parsed_keys']['highlight'].append(value)
                command['keys'].pop('clr2')
            except:
                return False
    return True

def run_command(client_id, account_id, type, command_keys, player):
    set_skincolor(player, command_keys['color'], command_keys['highlight'])

def set_skincolor(cl_id, color, highlight):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if len(color) == 1:
                    activity.change_node_color(player.actor.node, 'color', color[0], k=1.2)
                elif len(color) == 3:
                    activity.change_node_color(player.actor.node, 'color', tuple(color))
                if len(highlight) == 1:
                    activity.change_node_color(player.actor.node, 'highlight', highlight[0], k=1.2)
                elif len(highlight) == 3:
                    activity.change_node_color(player.actor.node, 'highlight', tuple(highlight))
