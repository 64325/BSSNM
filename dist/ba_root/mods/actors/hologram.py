from __future__ import annotations  # Импорт для поддержки аннотаций в старых версиях Python

import random
import math
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class Hologram(ba.Actor):

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 orientation: Sequence[float] = (1.0, 0.0, 0.0, 0.0),
                 size: float = 1.0,
                 model: str = 'shield',
                 texture: str = 'shield',
                 color: Sequence[float] = (0.2, 0.8, 1.0)
                ):
        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты из игры
        activity = self.getactivity()  # Получаем текущую активность

        hmats = [getHologramMaterial()]  # Получаем материалы голограммы

        # Создаем новый узел для голограммы
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel(model),
                                   'color_texture': ba.gettexture(texture),
                                   'body': 'crate',
                                   'reflection': 'soft',
                                   'reflection_scale': color,
                                   'shadow_size': 0.0,
                                   'is_area_of_interest': False,
                                   'position': position,
                                   'materials': hmats,
                                   'body_scale': 0.01,
                                   'model_scale': size,
                                   'gravity_scale': 0.0
                               })
        
        # Устанавливаем ориентацию узла голограммы
        self.node.handlemessage('set_q', orientation[0], orientation[1], orientation[2], orientation[3])
        
        # Анимируем масштаб модели голограммы
        ba.animate(self.node, 'model_scale', {0: 0, 0.2: 1.3 * size, 0.26: 1 * size})
        
        self.owner = None  # Инициализируем владельца голограммы как None

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            self.node.delete()  # Удаляем узел при получении сообщения о смерти
        elif isinstance(msg, ba.OutOfBoundsMessage):
            pass  # Ничего не делаем при выходе за границы
        else:
            super().handlemessage(msg)  # Обрабатываем остальные сообщения базовым методом

def getHologramMaterial():
    shared = SharedObjects.get()  # Получаем общие объекты из игры

    material = ba.Material()  # Создаем новый материал для голограммы
    material.add_actions(actions=('modify_part_collision',
                                  'collide', False))  # Отключаем столкновения для частей
    material.add_actions(actions=('modify_node_collision',
                                  'collide', False))  # Отключаем столкновения для узлов
    return material

def getRegionMaterial():
    shared = SharedObjects.get()  # Получаем общие объекты из игры

    material = ba.Material()  # Создаем новый материал для региона
    
    # Устанавливаем действия для столкновений с различными материалами
    material.add_actions(conditions=('they_have_material',
                                     shared.pickup_material),
                         actions=('modify_node_collision',
                                  'collide', False))

    material.add_actions(conditions=('they_have_material',
                                     shared.pickup_material),
                         actions=('modify_part_collision',
                                  'collide', False))
    
    material.add_actions(conditions=('they_have_material',
                                     shared.object_material),
                         actions=('modify_node_collision',
                                  'collide', True))

    material.add_actions(conditions=('they_have_material',
                                     shared.object_material),
                         actions=('modify_part_collision',
                                  'collide', True))
        
    material.add_actions(conditions=('they_have_material',
                                     shared.player_material),
                         actions=('modify_node_collision',
                                  'collide', True))

    material.add_actions(conditions=('they_have_material',
                                     shared.player_material),
                         actions=('modify_part_collision',
                                  'collide', True))

    return material

def composition(seq1, seq2):
    arg1 = seq1[3] * math.pi / 180.0
    Q2 = (math.cos(arg1 / 2.0), math.sin(arg1 / 2.0) * seq1[0], math.sin(arg1 / 2.0) * seq1[1], math.sin(arg1 / 2.0) * seq1[2])
    arg2 = seq2[3] * math.pi / 180.0
    Q1 = (math.cos(arg2 / 2.0), math.sin(arg2 / 2.0) * seq2[0], math.sin(arg2 / 2.0) * seq2[1], math.sin(arg2 / 2.0) * seq2[2])
    s1 = Q1[0]
    x1 = Q1[1]
    y1 = Q1[2]
    z1 = Q1[3]
    s2 = Q2[0]
    x2 = Q2[1]
    y2 = Q2[2]
    z2 = Q2[3]
    s3 = s1 * s2 - x1 * x2 - y1 * y2 - z1 * z2
    x3 = s1 * x2 + s2 * x1 + y1 * z2 - y2 * z1
    y3 = s1 * y2 + s2 * y1 + z1 * x2 - z2 * x1
    z3 = s1 * z2 + s2 * z1 + x1 * y2 - x2 * y1
    cos3 = s3
    sin3 = math.sqrt(max(0.0, 1.0 - cos3 * cos3))
    arg3 = math.atan2(sin3, cos3) * 2.0
    if sin3 >= -0.00000001 and sin3 <= 0.00000001:
        return (1.0, 0.0, 0.0, 0.0)
    return (x3 / sin3, y3 / sin3, z3 / sin3, arg3 * 180.0 / math.pi)

def rotate_point(pos1, seq):
    arg = seq[3] * math.pi / 180.0
    Q1 = (math.cos(arg / 2.0), math.sin(arg / 2.0) * seq[0], math.sin(arg / 2.0) * seq[1], math.sin(arg / 2.0) * seq[2])
    Q2 = (0.0, pos1[0], pos1[1], pos1[2])
    s1 = Q1[0]
    x1 = Q1[1]
    y1 = Q1[2]
    z1 = Q1[3]
    s2 = Q2[0]
    x2 = Q2[1]
    y2 = Q2[2]
    z2 = Q2[3]
    s3 = s1 * s2 - x1 * x2 - y1 * y2 - z1 * z2
    x3 = s1 * x2 + s2 * x1 + y1 * z2 - y2 * z1
    y3 = s1 * y2 + s2 * y1 + z1 * x2 - z2 * x1
    z3 = s1 * z2 + s2 * z1 + x1 * y2 - x2 * y1
    Q1 = (s3, x3, y3, z3)
    Q2 = (math.cos(arg / 2.0), -math.sin(arg / 2.0) * seq[0], -math.sin(arg / 2.0) * seq[1], -math.sin(arg / 2.0) * seq[2])
    s1 = Q1[0]
    x1 = Q1[1]
    y1 = Q1[2]
    z1 = Q1[3]
    s2 = Q2[0]
    x2 = Q2[1]
    y2 = Q2[2]
    z2 = Q2[3]
    s3 = s1 * s2 - x1 * x2 - y1 * y2 - z1 * z2
    x3 = s1 * x2 + s2 * x1 + y1 * z2 - y2 * z1
    y3 = s1 * y2 + s2 * y1 + z1 * x2 - z2 * x1
    z3 = s1 * z2 + s2 * z1 + x1 * y2 - x2 * y1
    return (x3, y3, z3)

def get_position_and_orientation(pos, seq1, seq2):
    return rotate_point(pos, seq2), composition(seq1, seq2)
