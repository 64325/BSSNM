from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type


class Platform(ba.Actor):

    def __init__(self,
                 size: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 0.0),
                 materials: Sequence[ba.Material] = None):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        
        # Импорт материалов для узлов и регионов
        from actors.hologram import getHologramMaterial, getRegionMaterial
        hmats = [getHologramMaterial()]  # Материалы для узлов
        rmats = (getRegionMaterial(), shared.footing_material,
                 shared.object_material)  # Материалы для регионов

        # Настройки узлов объекта
        self.node_scale = 0.042 * size
        self.region_scale = size

        # Создание узла node1
        self.node1 = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('hockeyStadiumInner'),
                                   'color_texture': ba.gettexture('footballStadium'),
                                   'body': 'crate',
                                   'body_scale': 0.01,
                                   'model_scale': self.node_scale,
                                   'reflection': 'soft',
                                   'reflection_scale': [0.2, 0.5, 0.7],  # Масштаб отражений
                                   'shadow_size': 0.0,
                                   'is_area_of_interest': False,
                                   'position': (position[0], position[1] - 0.07 * size, position[2] - 0.25 * size),
                                   'materials': hmats,
                                   'gravity_scale': 0.0
                               })
        self.node1.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)

        # Создание узла node2
        self.node2 = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('hockeyStadiumInner'),
                                   'color_texture': ba.gettexture('footballStadium'),
                                   'body': 'crate',
                                   'body_scale': 0.01,
                                   'model_scale': self.node_scale,
                                   'reflection': 'soft',
                                   'reflection_scale': [0.2, 0.5, 0.7],  # Масштаб отражений
                                   'shadow_size': 0.0,
                                   'is_area_of_interest': False,
                                   'position': (position[0], position[1], position[2] + 0.25 * size),
                                   'materials': hmats,
                                   'gravity_scale': 0.0
                               })
        self.node2.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)

        # Создание региона
        self.region = ba.newnode('region',
                                 attrs={
                                     'position': position,
                                     'scale': (self.region_scale, self.region_scale * 0.05, self.region_scale),
                                     'type': 'box',
                                     'materials': rmats
                                 })
        self.owner = None

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            # Удаление узлов и региона при получении сообщения DieMessage
            self.node1.delete()
            self.node2.delete()
            self.region.delete()

        elif isinstance(msg, ba.OutOfBoundsMessage):
            # Обработка сообщения о выходе за границы
            pass

        elif isinstance(msg, ba.HitMessage):
            # Обработка сообщения о попадании
            pass

        else:
            # Обработка других сообщений
            pass
