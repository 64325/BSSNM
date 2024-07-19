from __future__ import annotations

import random
import math
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

try:
    from ba._generated.enums import InputType  # 1.7.6+
except:
    from ba._enums import InputType  # 1.7.5 and lower

from bastd.actor.bomb import Bomb

class Floater(ba.Actor):

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 0.0),
                 materials: Sequence[ba.Material] = None):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()

        self.cur_pos = (position[0], position[1], position[2])
        self.cur_vel = (0.0, 0.0, 0.0)

        # Импортируем материал для объекта и платформы из другого модуля
        from actors.hologram import getHologramMaterial
        pmats = [shared.object_material, shared.footing_material]
        vmats = [getHologramMaterial()]

        # Создаем узел для объекта, используя модель 'shield'
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('shield'),
                                   'color_texture': None,
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'reflection_scale': [0.1],
                                   'shadow_size': 0.0,
                                   'is_area_of_interest': True,
                                   'position': self.cur_pos,
                                   'materials': pmats,
                                   'body_scale': 1.2,
                                   'model_scale': 0.3,
                                   'gravity_scale': 0.0,
                                   'density': 5000.0
                               })

        # Создаем узел для платформы, используя модель 'flagStand'
        self.platform = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'model': ba.getmodel('flagStand'),
                                       'color_texture': ba.gettexture('bg'),
                                       'body': 'landMine',
                                       'reflection': 'soft',
                                       'reflection_scale': [0.3],
                                       'shadow_size': 0.0,
                                       'is_area_of_interest': True,
                                       'position': self.cur_pos,
                                       'materials': vmats,
                                       'body_scale': 1.15,
                                       'model_scale': 4.0,
                                       'gravity_scale': 0.0
                                   })

        # Создаем узел для шайбы, используя модель 'puck'
        self.puck = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('puck'),
                                   'color_texture': ba.gettexture('bg'),
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'reflection_scale': [0.5],
                                   'shadow_size': 0.0,
                                   'is_area_of_interest': False,
                                   'position': self.cur_pos,
                                   'materials': vmats,
                                   'body_scale': 0.01,
                                   'model_scale': 0.8,
                                   'gravity_scale': 0.0
                               })
        self.puck.handlemessage('set_q', 1.0, 0.0, 0.0, -90.0)

        # Создаем узел для щита, используя тип узла 'shield'
        self.shield = ba.newnode('shield',
                                 owner=None,
                                 attrs={
                                     'color': (1.5, 1.5, 1.5),
                                     'radius': 0.65
                                 })

        # Создаем узел для флага
        self.flag = ba.newnode('flag',
                               delegate=self,
                               attrs={
                                   'position': self.cur_pos,
                                   'color_texture': ba.gettexture('flagColor'),
                                   'color': (0.1, 0.1, 0.4),
                                   'materials': vmats
                               })

        # Инициализируем переменные состояния движения
        self.owner = None
        self.back_front_move = 0.0
        self.left_right_move = 0.0
        self.up_down_move = 0.0

        self.recharging = False

        # Запускаем методы для обработки физики и отрисовки объекта
        self._handle_vel()
        self._draw()
        #self._emit()

    def _handle_vel(self):
        # Обрабатываем текущую скорость объекта
        try:
            self.cur_vel = (self.cur_vel[0] + 0.002 * self.left_right_move,
                            self.cur_vel[1] + 0.0018 * self.up_down_move,
                            self.cur_vel[2] + 0.002 * self.back_front_move)
            v = self.cur_vel
            v_scale = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
            k = 0.0013 / max(0.0013, v_scale)
            self.cur_vel = (v[0] * (1.0 - k), v[1] * (1.0 - k), v[2] * (1.0 - k))

            # Запускаем обработку скорости через небольшой интервал времени
            ba.timer(0.005, self._handle_vel)
        except:
            pass

    def _draw(self):
        # Отрисовываем объект и его компоненты
        try:
            self.cur_pos = (self.cur_pos[0] + self.cur_vel[0],
                            self.cur_pos[1] + self.cur_vel[1],
                            self.cur_pos[2] + self.cur_vel[2])
            self.node.position = self.cur_pos
            self.platform.position = (self.node.position[0], self.node.position[1], self.node.position[2])
            self.puck.position = (self.node.position[0] - 0.2, self.node.position[1] + 0.2, self.node.position[2])
            self.shield.position = (self.node.position[0] - 0.2, self.node.position[1] + 0.3, self.node.position[2])
            self.flag.position = (self.node.position[0] + 0.5, self.node.position[1] + 0.4, self.node.position[2])

            # Запускаем отрисовку через небольшой интервал времени
            ba.timer(0.005, self._draw)
        except:
            pass

    def _emit(self):
        # Эмитируем эффекты частиц
        try:
            ba.emitfx(position=(self.cur_pos[0] + 1.0, self.cur_pos[1], self.cur_pos[2]),
                      velocity=(3.0, 0.0, 0.0),
                      count=1,
                      scale=2.0,
                      chunk_type='sweat',
                      spread=0.1
                      )

            # Запускаем эмиссию через небольшой интервал времени
            ba.timer(0.1, self._emit)
        except:
            pass

    def recharge(self):
        # Обновляем состояние перезарядки
        self.recharging = False

    def _press_left_right(self, value=0.0):
        # Обрабатываем движение влево и вправо
        self.left_right_move = value

    def _press_up_down(self, value=0.0):
        # Обрабатываем движение вверх и вниз
        self.back_front_move = -value

    def _pick_up_press(self):
        # Обрабатываем нажатие на поднятие
        self.up_down_move = 1.0

    def _pick_up_release(self):
        # Обрабатываем отпускание поднятия
        self.up_down_move = 0.0

    def _jump_press(self):
        # Обрабатываем нажатие на прыжок
        self.up_down_move = -1.0

    def _jump_release(self):
        # Обрабатываем отпускание прыжка
        self.up_down_move = 0.0

    def _punch_press(self):
        # Обрабатываем нажатие на удар
        self._disassign()

    def _bomb_press(self):
        # Обрабатываем нажатие на бомбу
        if not self.recharging:
            self.recharging = True
            ba.timer(0.1, self.recharge)
            Bomb(position=(self.cur_pos[0], self.cur_pos[1] - 1.5, self.cur_pos[2]), velocity=(0.0, -10.0, 0.0), bomb_scale=0.75, bomb_time=0.5).autoretain()

    def _assign(self, player):
        # Присваиваем игроку управление над объектом
        self.owner = player
        player.actor.connect_controls_to_player()
        player.actor.disconnect_controls_from_player()
        player.resetinput()
        player.assigninput(InputType.PICK_UP_PRESS, self._pick_up_press)
        player.assigninput(InputType.PICK_UP_RELEASE, self._pick_up_release)
        player.assigninput(InputType.JUMP_PRESS, self._jump_press)
        player.assigninput(InputType.JUMP_RELEASE, self._jump_release)
        player.assigninput(InputType.BOMB_PRESS, self._bomb_press)
        player.assigninput(InputType.PUNCH_PRESS, self._punch_press)
        player.assigninput(InputType.UP_DOWN, self._press_up_down)
        player.assigninput(InputType.LEFT_RIGHT, self._press_left_right)

    def _disassign(self):
        # Отменяем присвоение игроку управления
        try:
            activity = self._activity()
            for player in activity.players:
                if player == self.owner:
                    player.resetinput()
                    if player.actor:
                        if player.actor.node.hold_node == self.node:
                            player.actor.node.hold_node = None
                        player.actor.connect_controls_to_player()
        except:
            pass
        self.owner = None
        self.back_front_move = 0.0
        self.left_right_move = 0.0
        self.up_down_move = 0.0

    def handlemessage(self, msg: Any) -> Any:
        # Обрабатываем входящие сообщения
        if isinstance(msg, ba.DieMessage):
            self._disassign()
            self._delete()

        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())

        elif isinstance(msg, ba.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1],
                msg.force_direction[2])

        elif isinstance(msg, ba.PickedUpMessage):
            if self.owner is None:
                try:
                    activity = self._activity()
                    for player in activity.players:
                        if player.actor and player.actor.node == msg.node:
                            self._assign(player)
                            break
                except:
                    pass

        elif isinstance(msg, ba.DroppedMessage):
            if self.owner is not None and self.owner.actor and msg.node == self.owner.actor.node:
                self._disassign()

        else:
            super().handlemessage(msg)

    def _delete(self):
        # Удаляем все узлы объекта
        try:
            if self.node is not None:
                self.node.delete()
                self.node = None

            if self.platform is not None:
                self.platform.delete()
                self.platform = None

            if self.puck is not None:
                self.puck.delete()
                self.puck = None

            if self.shield is not None:
                self.shield.delete()
                self.shield = None

            if self.flag is not None:
                self.flag.delete()
                self.flag = None
        except:
            pass


def getBallMaterial():
    # Получаем материал для шара
    shared = SharedObjects.get()

    material = ba.Material()
    material.add_actions(actions=(('modify_part_collision',
                                   'friction', 2.5)))
    material.add_actions(
        conditions=(
            ('we_are_younger_than', 100),
            'and',
            ('they_have_material', shared.object_material),
        ),
        actions=('modify_node_collision', 'collide', False),
    )

    material.add_actions(
        conditions=('they_have_material', shared.footing_material),
        actions=('impact_sound', ba.getsound('footImpact01'), 0.2, 5))

    return material
