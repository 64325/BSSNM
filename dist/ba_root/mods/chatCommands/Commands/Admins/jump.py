import math

import ba, _ba

description = 'высокий прыжок'

using_players_ids = True

from bastd.actor.spaz import Spaz
old_on_jump_press = Spaz.on_jump_press
old_on_jump_release = Spaz.on_jump_release
old_on_move_up_down = Spaz.on_move_up_down
old_on_move_left_right = Spaz.on_move_left_right

def new_on_jump_press(self) -> None:
    old_on_jump_press(self)
    if hasattr(self, 'control_mode') and self.control_mode == 'highjump':
        if self.node and self.footing:
            ba.timer(0.01, ba.Call(_highjump_impulse, self, self.node.velocity[1]))

Spaz.on_jump_press = new_on_jump_press


def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    set_highjump(client_id, player)

def set_highjump(client_id, cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if hasattr(player.actor, 'control_mode') and player.actor.control_mode == 'highjump':
                    player.actor.control_mode = 'normal'
                else:
                    player.actor.control_mode = 'highjump'

def find_head(spaz):
    torso_pos = spaz.node.torso_position
    pos_center = spaz.node.position_center
    dist = (pos_center[0] - torso_pos[0],
            pos_center[1] - torso_pos[1],
            pos_center[2] - torso_pos[2])
    pos_head = (torso_pos[0] + 4.0 * dist[0],
                torso_pos[1] + 4.0 * dist[1],
                torso_pos[2] + 4.0 * dist[2])
    return pos_head

def _highjump_impulse(spaz, prev_velocity: float):
    try:
        pos_head = find_head(spaz)
        d = spaz.node.velocity[1] - 3.2
        if spaz.node.velocity[1] - prev_velocity > 2.0 and d > 0.0:
            spaz.node.handlemessage('kick_back', pos_head[0], pos_head[1], pos_head[2], 0.0, 1.0, 0.0, 140.0 * d)
            #spaz.node.handlemessage(
            #    'impulse', spaz.node.torso_position[0], spaz.node.torso_position[1], spaz.node.torso_position[2],
            #    0.0, 0.0, 0.0, 200.0 * d, 200.0 * d, 0.0, 0.0, 0.0, 1.0, 0.0)
        spaz.node.handlemessage('kick_back', pos_head[0], pos_head[1], pos_head[2], 0.0, 1.0, 0.0, 280.0)
        ba.emitfx(position=(spaz.node.torso_position[0],
                            spaz.node.torso_position[1] - 0.3,
                            spaz.node.torso_position[2]),
                  velocity=(0.0, 0.0, 0.0),
                  count=10,
                  scale=0.7,
                  chunk_type='spark',
                  spread=0.3)
    except:
        pass
