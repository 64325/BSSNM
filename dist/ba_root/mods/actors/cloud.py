from __future__ import annotations  # Используем новые возможности Python для аннотаций типов

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

from actors.hologram import Hologram
from actors.lighting import Lighting

class Cloud(Hologram):

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),  # Начальная позиция облака по умолчанию
                 size: float = 1.0,  # Размер облака по умолчанию
                 color = (0.043, 0.05, 0.07)):  # Цвет облака по умолчанию
        super().__init__(position=position)  # Вызываем конструктор родительского класса

        # Получаем общие объекты игры
        shared = SharedObjects.get()
        activity = self.getactivity()

        # Настраиваем цвет и размер облака
        self.node.color_texture = None
        activity.change_node_color(self.node, 'reflection_scale', color, k=0.46)
        self.owner = None
        self.size = 0.5 * size

        # Позиции для частей облака относительно центра
        self.parts_pos = [
            (-0.7 * self.size, 0.2 * self.size),
            (-0.2 * self.size, -0.5 * self.size),
            (-0.1 * self.size, 0.4 * self.size),
            (0.2 * self.size, 0.3 * self.size),
            (0.7 * self.size, 0.0 * self.size)
        ]

        self.lightings = []

        # Создаем освещение для каждой части облака
        for part_pos in self.parts_pos:
            mnode = ba.newnode('math',
                               owner=self.node,
                               attrs={
                                   'input1': (part_pos[0], 0, part_pos[1]),
                                   'operation': 'add'
                               })
            self.node.connectattr('position', mnode, 'input2')
            lighting = Lighting(size=2.3 * self.size, color=self.node.reflection_scale)
            lighting.owner = self.node
            self.lightings.append(lighting)
            mnode.connectattr('output', lighting.node, 'position')
            self.node.connectattr('reflection_scale', lighting.node, 'reflection_scale')

    def handlemessage(self, msg: Any) -> Any:
        # Обрабатываем сообщение о смерти объекта
        if isinstance(msg, ba.DieMessage):
            # Удаляем каждое освещение
            for lighting in self.lightings:
                lighting.handlemessage(ba.DieMessage())
            # Удаляем узел облака
            self.node.delete()

        elif isinstance(msg, ba.OutOfBoundsMessage):
            # Обработка выхода объекта за пределы игрового поля
            pass

        else:
            # Передаем сообщение родительскому классу для обработки
            super().handlemessage(msg)
