import math

import ba, _ba

description = '3d полёт'

using_players_ids = True

from bastd.actor.spaz import Spaz
old_on_jump_press = Spaz.on_jump_press
old_on_jump_release = Spaz.on_jump_release
old_on_move_up_down = Spaz.on_move_up_down
old_on_move_left_right = Spaz.on_move_left_right

def new_on_jump_press(self) -> None:
    if hasattr(self, 'control_mode') and self.control_mode == 'fly3d':
        fly3d_start(self)
    else:
        old_on_jump_press(self)

def new_on_jump_release(self) -> None:
    if hasattr(self, 'control_mode') and self.control_mode == 'fly3d':
        fly3d_stop(self)
    else:
        old_on_jump_release(self)

def new_on_move_up_down(self, value: float) -> None:
    old_on_move_up_down(self, value)
    if hasattr(self, 'control_mode') and self.control_mode == 'fly3d':
        _fly3d_move_up_down(self, value)

def new_on_move_left_right(self, value: float) -> None:
    old_on_move_left_right(self, value)
    if hasattr(self, 'control_mode') and self.control_mode == 'fly3d':
        _fly3d_move_left_right(self, value)

Spaz.on_jump_press = new_on_jump_press
Spaz.on_jump_release = new_on_jump_release
Spaz.on_move_up_down = new_on_move_up_down
Spaz.on_move_left_right = new_on_move_left_right


def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    set_fly3d(client_id, player)

def set_fly3d(client_id, cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if hasattr(player.actor, 'control_mode') and player.actor.control_mode == 'fly3d':
                player.actor.control_mode = 'normal'
                player.actor.fly3dTimer = None
            else:
                player.actor.control_mode = 'fly3d'
                player.actor.fly3d_up_down = 0.0
                player.actor.fly3d_left_right = 0.0
                player.actor.fly3dTimer = ba.Timer(0.05, ba.Call(_fly3d_impulse_hor, player.actor), repeat=True)

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

def fly3d_start(spaz):
    _fly3d_impulse_ver(spaz)
    spaz.fly3dUpTimer = ba.Timer(0.02, ba.Call(_fly3d_impulse_weak, spaz), repeat=True)

def fly3d_stop(spaz):
    spaz.fly3dUpTimer = None

def _fly3d_impulse_ver(spaz):
    if not spaz.node or spaz.node.frozen or spaz.node.knockout > 0.0:
        return
    try:
        pos_head = find_head(spaz)
        spaz.node.handlemessage('kick_back', pos_head[0], pos_head[1], pos_head[2], 0.0, 1.0, 0.0, 240.0)
    except:
        pass

def _fly3d_move_left_right(spaz, value = 0.0):
    spaz.fly3d_left_right = value

def _fly3d_move_up_down(spaz, value = 0.0):
    spaz.fly3d_up_down = value

def _fly3d_impulse_hor(spaz):
    if spaz.control_mode != 'fly3d':
        spaz.fly3dTimer = None
        return
    if not spaz.node or spaz.node.frozen or spaz.node.knockout > 0.0:
        return
    try:
        len = math.hypot(spaz.fly3d_left_right, spaz.fly3d_up_down)
        if len > 0.01:
            impulse = (spaz.fly3d_left_right / len, -spaz.fly3d_up_down / len)
            v = math.hypot(spaz.node.velocity[0], spaz.node.velocity[2])
            if v < 0.01:
                impulse_mag = 30.0
            else:
                v_hor = (spaz.node.velocity[0] / v, spaz.node.velocity[2] / v)
                dist = (impulse[0] - v_hor[0], impulse[1] - v_hor[1])
                dist_len = math.hypot(dist[0], dist[1])
                impulse_mag = 15.0 * (1.0 + 2.5 * dist_len)
            pos_head = find_head(spaz)
            spaz.node.handlemessage('kick_back', pos_head[0], pos_head[1], pos_head[2], impulse[0], 0.0, impulse[1], 3.0 * impulse_mag)
    except:
        pass

def _fly3d_impulse_weak(spaz):
    if not spaz.node or spaz.node.frozen or spaz.node.knockout > 0.0:
        return
    try:
        spaz.node.handlemessage('kick_back', spaz.node.position_center[0], spaz.node.position_center[1], spaz.node.position_center[2], 0.0, 1.0, 0.0, 180.0)
        ba.emitfx(position=spaz.node.torso_position,
                  emit_type='fairydust')
    except:
        pass