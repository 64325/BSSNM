from __future__ import annotations  # Используем новые аннотации типов

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class Ball(ba.Actor):
    
    def __init__(self,
                 size: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты
        activity = self.getactivity()  # Получаем активность
        
        ball_material = getBallMaterial()  # Получаем материал мяча
        ball_material.add_actions(actions=('call', 'at_connect', self.handle_hit))  # Добавляем действия материала
        bmats = [shared.object_material, ball_material]  # Список материалов для узла
        
        # Создаем узел мяча
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('frostyPelvis'),  # Модель мяча
                                   'color_texture': ba.gettexture('aliBSRemoteIOSQR'),  # Текстура цвета
                                   'body': 'sphere',  # Тип тела - сфера
                                   'reflection': 'soft',  # Мягкое отражение
                                   'reflection_scale': [0.1],  # Масштаб отражения
                                   'shadow_size': 0.5,  # Размер тени
                                   'is_area_of_interest': True,  # Область интереса
                                   'position': position,  # Позиция
                                   'materials': bmats,  # Материалы
                                   'body_scale': size,  # Масштаб тела
                                   'density': 1.45 / size / size * 0.8,  # Плотность
                                   'gravity_scale': 1.2  # Масштаб гравитации
                               })
        
        # Анимация изменения масштаба модели мяча
        ba.animate(self.node, 'model_scale', {0: 0, 0.2: 1.3 * size, 0.26: 1.0 * size})
        self.owner = None  # Владелец не определен

    def handle_hit(self):
        try:
            self.last_vel = self.node.velocity  # Запоминаем последнюю скорость
            ba.timer(0.02, self.increase_impulse)  # Запускаем таймер для увеличения импульса
        except:
            pass

    def increase_impulse(self):
        if not self.node:
            return
        k = 1.2  # Коэффициент увеличения импульса
        try:
            # Увеличиваем скорость узла
            self.node.velocity = (self.last_vel[0] + k * (self.node.velocity[0] - self.last_vel[0]),
                                  self.last_vel[1] + k * (self.node.velocity[1] - self.last_vel[1]),
                                  self.last_vel[2] + k * (self.node.velocity[2] - self.last_vel[2]))
            self.last_vel = self.node.velocity  # Обновляем последнюю скорость
        except:
            pass

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            self.node.delete()  # Удаляем узел при получении сообщения о смерти

        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())  # Обрабатываем сообщение об выходе за границы

        elif isinstance(msg, ba.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            # Обрабатываем сообщение о попадании
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1],
                msg.force_direction[2])

        else:
            super().handlemessage(msg)  # Обрабатываем сообщения по умолчанию

def getBallMaterial():
    shared = SharedObjects.get()  # Получаем общие объекты

    material = ba.Material()  # Создаем материал
    material.add_actions(actions=(('modify_part_collision',
                                   'friction', 1.5)))  # Добавляем действие изменения трения
    material.add_actions(
        conditions=(
            ('we_are_younger_than', 100),  # Условие: моложе 100
            'and',
            ('they_have_material', shared.object_material),  # Условие: есть материал объекта
        ),
        actions=('modify_node_collision', 'collide', False),  # Действие: отключить столкновения
    )

    material.add_actions(
        conditions=('they_have_material', shared.footing_material),  # Условие: есть материал основания
        actions=('impact_sound', ba.getsound('footImpact01'), 0.12, 4))  # Действие: звук удара

    return material  # Возвращаем материал
