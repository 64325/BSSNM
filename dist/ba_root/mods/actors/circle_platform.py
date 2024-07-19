from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class CirclePlatform(ba.Actor):

    def __init__(self,
                 size: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 0.0),
                 materials: Sequence[ba.Material] = None):
        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты
        activity = self.getactivity()  # Получаем текущую активность

        # Импортируем необходимые материалы
        from actors.hologram import getHologramMaterial, getRegionMaterial
        hmats = [getHologramMaterial()]
        rmats = (getRegionMaterial(), shared.footing_material,
                shared.object_material)

        # Устанавливаем параметры узла для отображения объекта
        self.node_scale = 2.4 * size
        self.region_scale = size
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('flagStand'),
                                   'color_texture': ba.gettexture('flagColor'),
                                   'body': 'crate',
                                   'body_scale': 0.01,
                                   'model_scale': self.node_scale,
                                   'reflection': 'soft',
                                   #'reflection_scale': [-0.3, -0.7, -1.5],
                                   #  0: [-0.6, -1.4, -3.0]  1: [-0.15, -0.35, -0.75]
                                   'reflection_scale': [-0.24 + 0.08 * 3.0 * color[0], -0.54 + 0.18 * 3.0 * color[1], -1.5 + 0.5 * 3.0 * color[2]],
                                   'shadow_size': 0.0,
                                   'is_area_of_interest': False,
                                   'position': position,
                                   'materials': hmats,
                                   'gravity_scale': 0.0
                               })
        self.node.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)

        # Создаем область региона и устанавливаем её параметры
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
            self.node.delete()  # Удаляем узел объекта
            self.region.delete()  # Удаляем регион

        elif isinstance(msg, ba.OutOfBoundsMessage):
            pass  # Обработка сообщения о выходе за границы

        elif isinstance(msg, ba.HitMessage):
            pass  # Обработка сообщения о попадании

        else:
            pass  # Другие сообщения
