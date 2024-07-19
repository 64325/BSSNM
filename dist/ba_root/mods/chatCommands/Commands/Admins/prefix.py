import math

import ba, _ba

aliases = ['tag']
description = 'установить тэг'
info = [
    '                                   установить тэг',
    '               /prefix   номер игрока или pb-id   текст',
    '                                  доп. параметры',
    '    size=размер   clr=цвет   t=интервалы(для анимации)',
    '                                      удалить тэг',
    '                    /prefix del   номер игрока или pb-id'
]

using_players_ids = True
using_pb_ids = True
using_string_arg = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'del' in command['args']:
        command['args'].remove('del')
        command['parsed_keys']['action'] = 'delete'
        return True
    command['parsed_keys']['action'] = 'set'
    if 'size' in command['keys'] and len(command['keys']['size']) == 1:
        try:
            command['parsed_keys']['size'] = float(command['keys']['size'][0])
            command['keys'].pop('size')
        except:
            return False
    from ba._activity import actor_colors, actor_animations
    command['parsed_keys']['colors'] = []
    command['parsed_keys']['t'] = []
    if 'clr' in command['keys']:
        if len(command['keys']['clr']) == 1:
            color = command['keys']['clr'][0]
            command['keys'].pop('clr')
            if color not in actor_colors and color not in actor_animations:
                showmessage(client_id, command['type'], color + ': цвет не найден', _red_)
                return False
            elif color in actor_animations:
                command['parsed_keys']['colors'] = actor_animations[color]['colors']
                command['parsed_keys']['t'] = actor_animations[color]['time_intervals']
                command['parsed_keys']['gradient'] = actor_animations[color]['gradient']
            else:
                command['parsed_keys']['colors'] = [color]
        elif len(command['keys']['clr']) == 3:
            try:
                color = []
                for i in range(3):
                    value = float(command['keys']['clr'][0])
                    command['keys']['clr'].pop(0)
                    color.append(value)
                command['keys'].pop('clr')
                command['parsed_keys']['colors'] = [color]
            except:
                return False
    elif 'clr1' in command['keys']:
        command['parsed_keys']['colors'] = []
        for i in range(5):
            attr = 'clr' + str(i + 1)
            if attr in command['keys']:
                if len(command['keys'][attr]) == 1:
                    color = command['keys'][attr][0]
                    command['keys'].pop(attr)
                    if color not in actor_colors:
                        showmessage(client_id, command['type'], color + ': цвет не найден', _red_)
                        return False
                    command['parsed_keys']['colors'].append(color)
                elif len(command['keys'][attr]) == 3:
                    try:
                        color = []
                        for i in range(3):
                            value = float(command['keys'][attr][0])
                            command['keys'][attr].pop(0)
                            color.append(value)
                        command['keys'].pop(attr)
                        command['parsed_keys']['colors'].append(color)
                    except:
                        return False
    if 't' in command['keys']:
        command['parsed_keys']['t'] = []
        if len(command['keys']['t']) == 0:
            return False
        while len(command['keys']['t']) > 0:
            try:
                value = min(1000, max(0.05, float(command['keys']['t'][0])))
                command['keys']['t'].pop(0)
                command['parsed_keys']['t'].append(value)
            except:
                return False
        command['keys'].pop('t')
    if 'gradient' in command['args']:
        command['args'].remove('gradient')
        command['parsed_keys']['gradient'] = True
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    from chatHandle.chat_functions import showmessage, _red_
    if command_keys['action'] == 'delete':
        remove_tag(pb_id)
    else:
        text = command_keys['string_arg']
        session = ba.getactivity().session
        text = ''
        size = 1.0
        colors = ['black']
        time_intervals = []
        gradient = False
        if pb_id in session.playersData['effects'] and 'tag' in session.playersData['effects'][pb_id]:
            text = session.playersData['effects'][pb_id]['tag']['text']
            if 'size' in session.playersData['effects'][pb_id]['tag']:
                size = session.playersData['effects'][pb_id]['tag']['size']
            if 'color' in session.playersData['effects'][pb_id]['tag']:
                colors = [session.playersData['effects'][pb_id]['tag']['color']]
            elif 'animation' in session.playersData['effects'][pb_id]['tag']:
                colors = session.playersData['effects'][pb_id]['tag']['animation']['colors']
                if 'time_intervals' in session.playersData['effects'][pb_id]['tag']['animation']:
                    time_intervals = session.playersData['effects'][pb_id]['tag']['animation']['time_intervals']
                if 'gradient' in session.playersData['effects'][pb_id]['tag']['animation']:
                    gradient = session.playersData['effects'][pb_id]['tag']['animation']['gradient']
        if command_keys['string_arg'] != '':
            text = command_keys['string_arg']
        if 'size' in command_keys:
            size = command_keys['size']
        if len(command_keys['colors']) != 0:
            colors = command_keys['colors']
            if len(command_keys['colors']) == 1:
                time_intervals = []
        if len(command_keys['t']) != 0:
            time_intervals = command_keys['t']
        if 'gradient' in command_keys:
            gradient = command_keys['gradient']
        set_tag(client_id, account_id, type, pb_id, acc_name, text, size, colors, time_intervals, gradient)

def remove_tag(pb_id):
    from ModData import effects
    effects.remove_effect(pb_id, 'tag')
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.remove_tag()

def set_tag(client_id, account_id, type, pb_id, acc_name, text, size, colors, time_intervals, gradient):
    from chatHandle.chat_functions import showmessage, _red_
    if text == '':
        showmessage(client_id, type, 'у игрока ' + pb_id + ' нет тэга, задайте новый', _red_)
        return
    from ModData import effects
    if len(colors) == 1 and len(time_intervals) == 0:
        attrs = {
            'text': text,
            'size': size,
            'color': colors[0]
        }
    else:
        if len(time_intervals) == 0:
            time_intervals = [0.5]
        attrs = {
            'text': text,
            'size': size,
            'animation': {
                'colors': colors,
                'time_intervals': time_intervals,
                'gradient': gradient
            }
        }
    effects.add_effect(pb_id, acc_name, 'tag', attrs)
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.set_tag()
