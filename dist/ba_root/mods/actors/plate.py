from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type


class Plate(ba.Actor):

    def __init__(self,
                 type: int = 1,  # Тип пластины: 1, 2 или 3
                 size: float = 1,  # Размер пластины
                 position: Sequence[float] = (0.0, 1.0, 0.0),  # Позиция пластины в пространстве
                 color: Sequence[float] = (1.0, 1.0, 0.0),  # Цвет пластины
                 materials: Sequence[ba.Material] = None):  # Материалы для региона пластины
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        from bastd.actor.bomb import BombFactory
        factory = BombFactory.get()

        tnt_mat = factory.bomb_material
        tnt_mat.add_actions(actions=(('modify_part_collision',
                                       'friction', 1.5)))
        
        from actors.hologram import getHologramMaterial, getRegionMaterial
        hmats = [getHologramMaterial()]
        rmats = (getRegionMaterial(), shared.footing_material,
                shared.object_material)

        # Вычисление масштабов узла и региона в зависимости от типа пластины
        k = 0.95
        if type == 1:
            node_scale = (k * size, k * 0.1 * min(2.0, size), k * size)
            region_scale = (size, 0.1 * min(2.0, size), size)
            self._spawn_pos = (position[0], position[1] - 0.075 * min(2.0, size), position[2])
        elif type == 2:
            node_scale = (k * 0.1 * min(2.0, size), k * size, k * size)
            region_scale = (0.1 * min(2.0, size), size, size)
            self._spawn_pos = (position[0], position[1], position[2])
        elif type == 3:
            node_scale = (k * size, k * size, k * 0.1 * min(2.0, size))
            region_scale = (size, size, 0.1 * min(2.0, size))
            self._spawn_pos = (position[0], position[1], position[2])
        else:
            print('неправильный тип')
            return

        # Создание узла пластины
        self.node = ba.newnode('locator',
                               delegate=self,
                               attrs={
                                   'shape': 'box',
                                   'size': node_scale,
                                   'position': self._spawn_pos,
                                   'color': color
                               })

        # Создание региона пластины
        self.region = ba.newnode('region',
                                 attrs={
                                     'type': 'box',
                                     'position': self._spawn_pos,
                                     'scale': region_scale,
                                     'materials': rmats
                                 })
        self.owner = None  # Владелец пластины (не используется в данном коде)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):  # Обработка сообщения о смерти
            self.node.delete()
            self.region.delete()

        elif isinstance(msg, ba.OutOfBoundsMessage):  # Обработка сообщения о выходе за границы
            pass  # В данном случае не обрабатываем

        elif isinstance(msg, ba.HitMessage):  # Обработка сообщения о попадании
            pass  # В данном случае не обрабатываем

        else:
            pass  # Все остальные сообщения не обрабатываем
