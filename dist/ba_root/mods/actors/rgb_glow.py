from __future__ import annotations

import time
import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class RGBGlow(ba.Actor):

    def __init__(self,
                 source_actor,
                 size = 1.0,
                 color = (1.0, 1.0, 1.0),
                 position = (0.0, 0.0, 0.0)):

        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        self.owner = None

        # Устанавливаем размер и цвет свечения
        self.size = 0.17 * max(0.01, min(4.0, size))

        # Создаем светящийся эффект вокруг указанного актера
        if source_actor and source_actor.node:
            self.node = ba.newnode('light',
                                   owner=source_actor.node,
                                   attrs={
                                       'position': position,
                                       'color': color,
                                       'height_attenuated': False,
                                       'radius': self.size
                                   })
            source_actor.node.connectattr('torso_position', self.node, 'position')

        # Анимируем радиус светового эффекта
        ba.animate(self.node, 'radius', {0: 0 * self.size, 0.2: 1.3 * self.size, 0.26: 1 * self.size})

    def handlemessage(self, msg: Any) -> Any:
        # Обрабатываем сообщения
        if isinstance(msg, ba.DieMessage):
            self.node.delete()
