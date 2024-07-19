from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class IceBall(ba.Actor):

    def __init__(self,
                 size: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты игры
        activity = self.getactivity()  # Получаем текущую активность игры

        ball_material = getBallMaterial()  # Получаем материал для мяча
        ball_material.add_actions(actions=('call', 'at_connect', self.handle_hit))  # Добавляем действия для материала мяча при столкновении
        bmats = [shared.object_material, ball_material]  # Список материалов для узла мяча
        from actors.hologram import getHologramMaterial  # Импортируем материал голограммы
        vmats = [getHologramMaterial()]  # Список материалов для узла голограммы

        if size <= 0.6:
            spaz_model = 'frostyTorso'  # Модель для маленького мяча
            body_scale = 0.8
            density = 1.1 * 1.4  # Плотность маленького мяча
            self.distance = -0.2
        elif size <= 1.1:
            spaz_model = 'frostyPelvis'  # Модель для среднего мяча
            body_scale = 1.0
            density = 1.12 * 1.15  # Плотность среднего мяча
            self.distance = 0.0
        else:
            spaz_model = 'shield'  # Модель для большого мяча
            body_scale = 3.2
            density = 0.07  # Плотность большого мяча
            self.distance = 0.0

        density *= 0.7  # Уменьшаем плотность

        # Создаем узел мяча
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': None,
                                   'color_texture': ba.gettexture('puckColor'),
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'reflection_scale': [0.1],
                                   'shadow_size': 0.5,
                                   'is_area_of_interest': True,
                                   'position': position,
                                   'materials': bmats,
                                   'body_scale': body_scale,
                                   'model_scale': body_scale,
                                   'density': density,
                                   'gravity_scale': 1.35
                               })
        self.owner = None
        
        color_k = 0.7 * 1.2  # Коэффициент для цвета
        color = (color[0] * color_k, color[1] * color_k, color[2] * color_k)  # Изменяем цвет
        color_res = (color[0] * 0.8 - 0.06, color[1] * 0.7 - 0.07, color[2] * 0.6 - 0.35)  # Рассчитываем окончательный цвет для спаза
        # Создаем узел спаза
        self.spaz: ba.Node = ba.newnode(
            type='spaz',
            delegate=self,
            attrs={
                'color': color_res,
                'behavior_version': 1,
                'demo_mode': False,
                'highlight': color_res,
                'color_texture': ba.gettexture('tipTopBGColor'),
                'color_mask_texture': ba.gettexture('characterIconMask'),
                'head_model': None,
                'torso_model': ba.getmodel(spaz_model),
                'pelvis_model': None,
                'upper_arm_model': None,
                'forearm_model': None,
                'hand_model': None,
                'upper_leg_model': None,
                'lower_leg_model': None,
                'toes_model': None,
                'style': 'cyborg',
                'fly': False,
                'hockey': False,
                'materials': vmats,
                'roller_materials': vmats,
                'extras_material': vmats,
                'punch_materials': vmats,
                'pickup_materials': vmats,
                'invincible': False,
                'source_player': None,
            })
        self.spaz.frozen = True  # Замораживаем спаза

        self._move_spaz()  # Запускаем функцию для движения спаза

    def handle_hit(self):
        try:
            self.last_vel = self.node.velocity  # Сохраняем последнюю скорость узла мяча
            ba.timer(0.02, self.increase_impulse)  # Устанавливаем таймер для увеличения импульса
        except:
            pass

    def increase_impulse(self):
        if not self.node:
            return
        k = 1.35  # Коэффициент увеличения импульса
        try:
            # Увеличиваем скорость узла мяча
            self.node.velocity = (self.last_vel[0] + k * (self.node.velocity[0] - self.last_vel[0]),
                                  self.last_vel[1] + k * (self.node.velocity[1] - self.last_vel[1]),
                                  self.last_vel[2] + k * (self.node.velocity[2] - self.last_vel[2]))
            self.last_vel = self.node.velocity
        except:
            pass
    
    def _move_spaz(self):
        try:
            pos = (self.node.position[0], self.node.position[1] - 1.0 + self.distance, self.node.position[2])
            self.spaz.handlemessage('stand', pos[0], pos[1], pos[2], 0)  # Отправляем сообщение для перемещения спаза
            ba.timer(0.005, self._move_spaz)  # Устанавливаем таймер для продолжения движения
        except:
            pass 

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            self.node.delete()  # Удаляем узел мяча
            self.spaz.delete()  # Удаляем узел спаза

        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())  # Обрабатываем выход за границы игрового поля

        elif isinstance(msg, ba.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            # Передаем сообщение узлу мяча о столкновении
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1],
                msg.force_direction[2])
            
        else:
            super().handlemessage(msg)  # Обрабатываем остальные сообщения

def getBallMaterial():
    shared = SharedObjects.get()  # Получаем общие объекты игры

    material = ba.Material()  # Создаем материал для мяча
    material.add_actions(actions=(('modify_part_collision',
                                   'friction', 2.5)))  # Добавляем действия для коллизий

    material.add_actions(
        conditions=(
            ('we_are_younger_than', 100),  # Условие на возраст материала
            'and',
            ('they_have_material', shared.object_material),  # Условие на наличие материала у других объектов
        ),
        actions=('modify_node_collision', 'collide', False),  # Действия при коллизии
    )

    material.add_actions(
        conditions=('they_have_material', shared.footing_material),  # Условие на наличие материала под ногами
        actions=('impact_sound', ba.getsound('footImpact01'), 0.12, 4)  # Звук при ударе
    )

    return material  # Возвращаем материал для мяча
