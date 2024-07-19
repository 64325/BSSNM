from __future__ import annotations  # Импорт новых возможностей из будущих версий Python

import time
import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

class Tag(ba.Actor):  # Определение базового класса Tag, наследующего ba.Actor

    def __init__(self,
                 source_actor,  # Инициализация конструктора
                 offset=(0.0, 1.2),  # Смещение текста по умолчанию
                 text='',  # Текстовое содержимое
                 size=1.0,  # Размер текста
                 color=(0.0, 0.0, 0.0),  # Цвет текста
                 position=(0.0, 0.0, 0.0)):  # Позиция текста в мировых координатах

        super().__init__()  # Вызов конструктора базового класса
        shared = SharedObjects.get()  # Получение общих объектов игры
        activity = self.getactivity()  # Получение текущей активности
        self.owner = None  # Инициализация владельца тега

        self.size = 0.012 * max(0.1, min(4.0, size))  # Вычисление финального размера текста

        if source_actor and source_actor.node:
            # Создание узла текста и его настройка
            self.node = ba.newnode('text',
                                   owner=source_actor.node,
                                   attrs={
                                       'text': text,
                                       'in_world': True,
                                       'shadow': 1.0,
                                       'flatness': 1.0,
                                       'scale': self.size,
                                       'color': color,
                                       'h_align': 'center',
                                       'position': position
                                   })
            # Создание математического узла для вычисления позиции текста
            mnode = ba.newnode('math',
                               owner=self.owner,
                               attrs={
                                   'input1': (offset[0], offset[1], 0),
                                   'operation': 'add'
                               })
            # Подключение узлов для установки позиции текста относительно актора
            source_actor.node.connectattr('torso_position', mnode, 'input2')
            mnode.connectattr('output', self.node, 'position')

            # Анимация масштабирования текста
            ba.animate(self.node, 'scale', {0: 0 * self.size, 0.2: 1.3 * self.size, 0.26: 1 * self.size})

    def handlemessage(self, msg: Any) -> Any:  # Обработчик сообщений актора
        if isinstance(msg, ba.DieMessage):  # Если получено сообщение о смерти
            self.node.delete()  # Удалить узел текста

class RankTag(Tag):  # Определение подкласса RankTag, наследующего Tag

    def __init__(self,
                 source_actor,  # Инициализация конструктора
                 rank,  # Ранг для отображения
                 color=(0.8, 0.8, 0.8),  # Цвет текста по умолчанию
                 position=(0.0, 0.0, 0.0)):  # Позиция текста в мировых координатах

        if hasattr(source_actor, 'tag') and source_actor.tag != None:
            offset = (0.0, 1.6)  # Смещение для особых случаев, когда у актора уже есть тег
            size = 0.64  # Размер текста для особых случаев
        else:
            offset = (0.0, 1.3)  # Стандартное смещение текста
            size = 0.78  # Стандартный размер текста

        super().__init__(source_actor,
                         offset,
                         text='#' + str(rank),  # Формирование текста с номером ранга
                         size=size,
                         color=color)  # Вызов конструктора родительского класса с параметрами
