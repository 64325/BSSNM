from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class Block(ba.Actor):

    def __init__(self,
                 size: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 0.0)):
        super().__init__()

        # Получаем общие объекты игры
        shared = SharedObjects.get()
        
        # Получаем активность, в которой создается блок
        activity = self.getactivity()

        # Импортируем материалы для голограммы и региона
        from actors.hologram import getHologramMaterial, getRegionMaterial
        hmats = [getHologramMaterial()]
        rmats = (getRegionMaterial(), shared.footing_material,
                 shared.object_material)

        # Настройки узла объекта блока
        self.node_scale = 1.6 * size
        self.region_scale = size
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('powerup'),
                                   'color_texture': ba.gettexture('flagColor'),
                                   'body': 'crate',
                                   'body_scale': 0.01,
                                   'model_scale': self.node_scale,
                                   'reflection': 'soft',
                                   'reflection_scale': [-0.24 + 0.08 * 3.0 * color[0], -0.54 + 0.18 * 3.0 * color[1], -1.5 + 0.5 * 3.0 * color[2]],
                                   'shadow_size': 0.0,
                                   'is_area_of_interest': False,
                                   'position': position,
                                   'materials': hmats,
                                   'gravity_scale': 0.0
                               })
        self.node.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)

        # Создаем регион для области вокруг блока
        self.region = ba.newnode('region',
                                 attrs={
                                     'position': position,
                                     'scale': (self.region_scale, self.region_scale, self.region_scale),
                                     'type': 'box',
                                     'materials': rmats
                                 })
        self.owner = None


    def handlemessage(self, msg: Any) -> Any:
        # Обработка сообщения о смерти актора
        if isinstance(msg, ba.DieMessage):
            self.node.delete()
            self.region.delete()

        # Обработка сообщения о выходе за границы
        elif isinstance(msg, ba.OutOfBoundsMessage):
            pass

        # Обработка сообщения о попадании
        elif isinstance(msg, ba.HitMessage):
            pass

        # Обработка остальных сообщений
        else:
            pass
