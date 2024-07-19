from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class Puck(ba.Actor):
    """A lovely giant hockey puck."""

    def __init__(self, position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        
        # Создаем материал для объекта
        material = ba.Material()
        material.add_actions(actions=(('modify_part_collision',
                                       'friction', 0.1)))
        
        # Настройки для взаимодействия с различными материалами
        material.add_actions(conditions=('they_have_material',
                                         shared.pickup_material),
                             actions=('modify_part_collision',
                                      'collide', False))
        
        material.add_actions(
            conditions=(
                ('we_are_younger_than', 100),
                'and',
                ('they_have_material', shared.object_material),
            ),
            actions=('modify_node_collision', 'collide', False),
        )
        
        material.add_actions(conditions=('they_have_material',
                                         shared.footing_material),
                             actions=('impact_sound',
                                      ba.getsound('metalHit'), 0.2, 5))

        pmats = [shared.object_material, material]
        
        # Создаем узел для модели объекта пака
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('puck'),
                                   'color_texture': ba.gettexture('puckColor'),
                                   'body': 'puck',
                                   'reflection': 'soft',
                                   'reflection_scale': [0.2],
                                   'shadow_size': 1.0,
                                   'is_area_of_interest': True,
                                   'position': position,
                                   'materials': pmats
                               })
        
        # Анимация масштабирования модели пака
        ba.animate(self.node, 'model_scale', {0: 0, 0.2: 1.3, 0.26: 1})

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            self.node.delete()

        # Если пак выходит за пределы игрового поля, удаляем его
        elif isinstance(msg, ba.OutOfBoundsMessage):
            handlemessage(ba.DieMessage())  # Возможно, нужно вызвать DieMessage()

        # Если пак получает удар, передаем сообщение узлу
        elif isinstance(msg, ba.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1],
                msg.force_direction[2])
        else:
            super().handlemessage(msg)
