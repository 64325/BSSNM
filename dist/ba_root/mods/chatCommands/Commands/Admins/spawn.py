import random

import ba, _ba

description = 'заспавнить предмет'

using_players_ids = True
timer_compatible = True

subtypes = objects = [
    'ball',
    'iceball',
    'puck',
    'flag',
    'freezebox',
    'freezebomb',
    'deathbomb',
    'mine',
    'tnt',
    'box',
    'block',
    'circle',
    'lift',
    'platform',
    'plate',
    'plate2',
    'plate3',
    'floater',
    'spaz',
    'agent',
    'frosty',
    'ninjabot'
]

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'list' in command['args']:
        command['args'].remove('list')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            return False
        return True
    if 'l' in command['args']:
        command['args'].remove('l')
        command['parsed_keys']['action'] = 'show'
        if len(command['args']) != 0:
            return False
        return True
    command['parsed_keys']['action'] = 'spawn'
    if len(command['args']) == 0:
        showmessage(client_id, command['type'], 'укажите предмет', _red_)
        return False
    object = command['args'][0]
    command['args'].pop(0)
    if object not in objects:
        showmessage(client_id, command['type'], object + ': предмет не найден', _red_)
        return False
    command['parsed_keys']['object'] = object
    command['subtype'] = object
    if 'c' in command['keys'] and len(command['keys']['c']) == 1:
        try:
            command['parsed_keys']['count'] = min(20, max(1, int(command['keys']['c'][0])))
            command['keys'].pop('c')
        except:
            return False
    if 'size' in command['keys'] and len(command['keys']['size']) == 1:
        try:
            command['parsed_keys']['size'] = max(0.2, float(command['keys']['size'][0]))
            command['keys'].pop('size')
        except:
            return False
    from ba._activity import actor_colors, get_color
    if 'clr' in command['keys']:
        if len(command['keys']['clr']) == 1:
            color = command['keys']['clr'][0]
            command['keys'].pop('clr')
            if color not in actor_colors:
                showmessage(client_id, command['type'], color + ': цвет не найден', _red_)
                return False
            command['parsed_keys']['color'] = color
        elif len(command['keys']['clr']) == 3:
            command['parsed_keys']['color'] = []
            try:
                for i in range(3):
                    value = float(command['keys']['clr'][0])
                    command['keys']['clr'].pop(0)
                    command['parsed_keys']['color'].append(value)
                command['keys'].pop('clr')
            except:
                return False
    if 'pos' in command['keys'] and len(command['keys']['pos']) == 3:
        command['parsed_keys']['position'] = []
        try:
            for i in range(3):
                value = float(command['keys']['pos'][0])
                command['keys']['pos'].pop(0)
                command['parsed_keys']['position'].append(value)
            command['keys'].pop('pos')
        except:
            return False
    if 'd' in command['keys'] and len(command['keys']['d']) == 3:
        command['parsed_keys']['dist'] = []
        try:
            for i in range(3):
                value = float(command['keys']['d'][0])
                command['keys']['d'].pop(0)
                command['parsed_keys']['dist'].append(value)
            command['keys'].pop('d')
        except:
            return False
    return True

def run_command(client_id, account_id, type, command_keys, player):
    if command_keys['action'] == 'show':
       show_objects(client_id, type)
       return
    if 'count' in command_keys:
        count = command_keys['count']
    else:
        count = 1
    if 'size' in command_keys:
        size = command_keys['size']
    else:
        size = 1.0
    if 'color' in command_keys:
        color = command_keys['color']
    else:
        color = None
    if 'position' in command_keys:
        position = command_keys['position']
    else:
        position = None
    if 'dist' in command_keys:
        dist = command_keys['dist']
    else:
        dist = None
    spawn_object(client_id, account_id, type, player, command_keys['object'], count, size, color, position, dist)

def spawn_object(client_id, account_id, type, cl_id, object_name, count, size, color, position, dist):
    from chatHandle.chat_functions import showmessage, _white_
    try:
        activity = ba.getactivity()
        session = activity.session
        if dist == None:
            if position == None:
                if object_name == 'mine':
                    dist = (0.0, -0.2 + 0.5 * size, 0.0)
                elif object_name == 'platform' or object_name == 'lift':
                    dist = (0.0, -0.4, 0.0)
                elif object_name == 'flag' or object_name == 'freezebox' or object_name == 'freezebomb' or object_name == 'deathbomb' or object_name == 'puck':
                    dist = (0.0, 0.0, 0.0)
                else:
                    dist = (0.0, 1.3, 0.0)
            else:
                dist = (0.0, 0.0, 0.0)
        target_player = None
        for player in activity.players:
            if player.sessionplayer.inputdevice.client_id == cl_id:
                if player.actor and player.actor.node:
                    target_player = player
        if target_player == None:
            if cl_id == client_id:
                if position == None:
                    position = (0.0, 5.0, 0.0)
                if color == None:
                    color = (1.0, 1.0, 1.0)
            else:
                return
        else:
            if position == None:
                position = target_player.actor.node.torso_position
            if color == None:
                color = target_player.actor.node.color
        from ba._activity import actor_colors, get_color
        position = (position[0] + dist[0], position[1] + dist[1], position[2] + dist[2])
        color_arg = color
        for i in range(count):
            color = get_color(color_arg)
            if target_player != None:
                highlight = target_player.actor.node.highlight
            else:
                highlight = color
            if object_name == 'flag':
                from bastd.actor.flag import Flag
                flag = Flag((position[0], position[1], position[2]), color).autoretain()
                flag.owner_id = cl_id
                activity.spawned_objects.append(flag)
            elif object_name == 'tnt':
                from bastd.actor.bomb import Bomb
                tnt = Bomb(position=position, bomb_type='tnt', bomb_scale=min(2.4, size)).autoretain()
                tnt.node.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)
                tnt.owner_id = cl_id
                activity.spawned_objects.append(tnt)
            elif object_name == 'freezebox':
                from actors.freeze_box import FreezeBox
                freeze_box = FreezeBox(position=position, bomb_scale=min(2.4, size)).autoretain()
                freeze_box.node.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)
                freeze_box.owner_id = cl_id
                activity.spawned_objects.append(freeze_box)
            elif object_name == 'freezebomb':
                from actors.freeze_bomb import FreezeBomb
                freeze_bomb = FreezeBomb(position=position, bomb_scale=min(2.4, size)).autoretain()
                freeze_bomb.owner_id = cl_id
                activity.spawned_objects.append(freeze_bomb)
            elif object_name == 'deathbomb':
                from actors.death_bomb import DeathBomb
                death_bomb = DeathBomb(position=position, bomb_scale=min(2.4, size)).autoretain()
                death_bomb.owner_id = cl_id
                activity.spawned_objects.append(death_bomb)
            elif object_name == 'mine':
                from actors.impact_mine import ImpactMine
                mine = ImpactMine(position=(position[0], position[1], position[2]), bomb_scale=min(2.4, size)).autoretain()
                mine.owner_id = cl_id
                activity.spawned_objects.append(mine)
            elif object_name == 'box':
                from actors.box import Box
                box = Box(size=min(2.3, size), position=position, color=color).autoretain()
                box.node.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)
                box.owner_id = cl_id
                activity.spawned_objects.append(box)
            elif object_name == 'block':
                from actors.block import Block
                block = Block(size=size, position=position, color=color).autoretain()
                block.owner_id = cl_id
                activity.spawned_objects.append(block)
            elif object_name == 'platform':
                from actors.platform import Platform
                platform = Platform(size=size, position=position, color=color).autoretain()
                platform.owner_id = cl_id
                activity.spawned_objects.append(platform)
            elif object_name == 'circle':
                from actors.circle_platform import CirclePlatform
                platform = CirclePlatform(size=size, position=position, color=color).autoretain()
                if target_player != None:
                    target_player.actor.node.handlemessage('stand', position[0], position[1] + 0.2, position[2], 0.0)
                platform.owner_id = cl_id
                activity.spawned_objects.append(platform)
            elif object_name == 'lift':
                from actors.lift import Lift
                lift = Lift(size=size, position=position, color=color).autoretain()
                lift.owner_id = cl_id
                activity.spawned_objects.append(lift)
            elif object_name == 'plate':
                from actors.plate import Plate
                plate = Plate(type=1, size=size, position=position, color=color).autoretain()
                plate.owner_id = cl_id
                activity.spawned_objects.append(plate)
            elif object_name == 'plate2':
                from actors.plate import Plate
                plate = Plate(type=2, size=size, position=position, color=color).autoretain()
                plate.owner_id = cl_id
                activity.spawned_objects.append(plate)
            elif object_name == 'plate3':
                from actors.plate import Plate
                plate = Plate(type=3, size=size, position=position, color=color).autoretain()
                plate.owner_id = cl_id
                activity.spawned_objects.append(plate)
            elif object_name == 'ball':
                from actors.ball import Ball
                ball = Ball(size=min(2.3, size), position=(position[0], position[1], position[2])).autoretain()
                ball.owner_id = cl_id
                activity.spawned_objects.append(ball)
            elif object_name == 'iceball':
                from actors.ice_ball import IceBall
                ice_ball = IceBall(size=min(2.0, size), position=(position[0], position[1], position[2]), color=color).autoretain()
                ice_ball.owner_id = cl_id
                activity.spawned_objects.append(ice_ball)
            elif object_name == 'puck':
                from actors.puck import Puck
                puck = Puck(position=(position[0], position[1], position[2])).autoretain()
                puck.owner_id = cl_id
                activity.spawned_objects.append(puck)
            elif object_name == 'spaz':
                from bastd.actor.spaz import Spaz
                spaz = Spaz(color=color, highlight=highlight, start_invincible=False).autoretain()
                spaz.handlemessage(ba.StandMessage(position, 0))
                spaz.owner_id = cl_id
                activity.spawned_objects.append(spaz)
            elif object_name == 'agent':
                from bastd.actor.spaz import Spaz
                spaz = Spaz(color=color, highlight=highlight, character='Agent Johnson', start_invincible=False).autoretain()
                spaz.handlemessage(ba.StandMessage(position, 0))
                spaz.owner_id = cl_id
                activity.spawned_objects.append(spaz)
            elif object_name == 'frosty':
                from bastd.actor.spaz import Spaz
                spaz = Spaz(color=color, highlight=highlight, character='Frosty', start_invincible=False).autoretain()
                spaz.handlemessage(ba.StandMessage(position, 0))
                spaz.owner_id = cl_id
                activity.spawned_objects.append(spaz)
            elif object_name == 'ninjabot':
                from bastd.actor.spazbot import ChargerBot, SpazBotSet
                if not hasattr(activity, '_bots'): activity._bots = SpazBotSet()
                activity._bots.spawn_bot(ChargerBot, pos=position, spawn_time=0.1)
            elif object_name == 'frostybot':
                from bastd.actor.spazbot import BrawlerBotProShielded, SpazBotSet
                if not hasattr(activity, '_bots'): activity._bots = SpazBotSet()
                activity._bots.spawn_bot(BrawlerBotProShielded, pos=position, spawn_time=0.1, color=color, highlight=highlight)
            elif object_name == 'zoebot':
                from bastd.actor.spazbot import TriggerBotProShielded, SpazBotSet
                if not hasattr(activity, '_bots'): activity._bots = SpazBotSet()
                activity._bots.spawn_bot(TriggerBotProShielded, pos=position, spawn_time=0.1, color=color, highlight=highlight)
            elif object_name == 'kronkbot':
                from bastd.actor.spazbot import BrawlerBotPro, SpazBotSet
                if not hasattr(activity, '_bots'): activity._bots = SpazBotSet()
                activity._bots.spawn_bot(BrawlerBotPro, pos=position, spawn_time=0.1, color=color, highlight=highlight)
            elif object_name == 'alibot':
                from bastd.actor.spazbot import BomberBotProShielded, SpazBotSet
                if not hasattr(activity, '_bots'): activity._bots = SpazBotSet()
                activity._bots.spawn_bot(BomberBotProShielded, pos=position, spawn_time=0.1, color=color, highlight=highlight)
            elif object_name == 'agentbot':
                from bastd.actor.spazbot import AgentBot, SpazBotSet
                if not hasattr(activity, '_bots'): activity._bots = SpazBotSet()
                activity._bots.spawn_bot(AgentBot, pos=position, spawn_time=0.1, color=color, highlight=highlight)
            elif object_name == 'floater':
                from actors.floater import Floater
                floater = Floater(position=position, color=color)
                floater.owner_id = cl_id
                activity.spawned_objects.append(floater)
    except:
        pass


def show_objects(client_id, type):
    type = 3 # вывод только в чат
    from chatHandle.chat_functions import showmessage, _white_
    showmessage(client_id, type, '=============== предметы: ===============', _white_)
    for object_name in objects:
        showmessage(client_id, type, '    ' + object_name, _white_)