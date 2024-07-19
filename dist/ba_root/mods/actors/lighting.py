from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

from actors.hologram import Hologram

class Lighting(Hologram):

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 size: float = 1.0,
                 color: Sequence[float] = (0, 0.05, 0.4)):
        super().__init__(position=position)

        # Получаем общие объекты игры
        shared = SharedObjects.get()
        # Получаем активность, в которой находится данный объект
        activity = self.getactivity()

        # Устанавливаем текстуру цвета узла в None
        self.node.color_texture = None
        # Изменяем цвет узла на указанный цвет
        activity.change_node_color(self.node, 'reflection_scale', color)
        self.owner = None

        # Устанавливаем размер световой вспышки
        self.size = size

        # Список для хранения взрывов
        self.explosions = []
        # Счетчик количества взрывов
        self.expl_count = 0

        # Таймер для создания световых вспышек
        self.lightTimer = ba.Timer(random.uniform(0.09, 0.11), self._spawn_lighting, repeat=True)

    def _spawn_lighting(self):
        try:
            # Создаем новую световую вспышку
            explosion = ba.newnode('explosion',
                                   attrs={
                                       'position': (self.node.position[0] + random.uniform(-0.05, 0.2) * self.size,
                                                    self.node.position[1] + random.uniform(-0.05, 0.2) * self.size,
                                                    self.node.position[2] + random.uniform(-0.05, 0.2) * self.size),
                                       'velocity': (0.0, 0.0, 0.0),
                                       'radius': 1.0 * self.size,
                                       'big': False,
                                       'color': self.node.reflection_scale
                                   })
            # Анимируем радиус взрыва
            ba.animate(explosion, 'radius', {0: 8.0 * self.size, 0.05: 2.0 * self.size, 0.17: 1.0 * self.size, 0.35: 2.0 * self.size})
            
            # Ограничиваем количество взрывов для уменьшения нагрузки
            if self.expl_count % 100 < 4:
                if self.expl_count % 100 == 0:
                    # Удаляем старые взрывы, чтобы избежать накопления
                    for old_expl in self.explosions:
                        if old_expl:
                            old_expl.delete()
                    self.explosions = []
                self.explosions.append(explosion)
            else:
                # Удаляем взрыв через некоторое время, если превышено максимальное количество
                ba.timer(0.2, explosion.delete)
            self.expl_count += 1
        except:
            # В случае исключения посылаем сообщение о смерти объекта
            self.handlemessage(ba.DieMessage())

    def handlemessage(self, msg: Any) -> Any:
        # Обработка сообщения о смерти объекта
        if isinstance(msg, ba.DieMessage):
            self.lightTimer = None
            # Удаляем все текущие взрывы
            for explosion in self.explosions:
                if explosion:
                    explosion.delete()

        # Обработка сообщения о выходе за границы
        elif isinstance(msg, ba.OutOfBoundsMessage):
            pass

        else:
            # Обработка остальных сообщений с помощью метода базового класса
            super().handlemessage(msg)
