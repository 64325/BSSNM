from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type


class Raindrop(ba.Actor):

    def __init__(self,
                 position: Sequence[float],
                 size: float = 1.0,
                 respawn = False):

        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты
        activity = self.getactivity()  # Получаем текущую активность

        # Импортируем материал для голограммы
        from actors.hologram import getHologramMaterial
        mats = [getHologramMaterial()]

        self._spawn_pos = position  # Устанавливаем позицию возрождения
        self.respawn = respawn  # Устанавливаем флаг возрождения
        # Создаем узел для объекта Raindrop
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('flagPole'),  # Модель объекта
                                   'color_texture': ba.gettexture('flagColor'),  # Текстура цвета
                                   'body': 'puck',  # Тип тела
                                   'reflection': 'soft',  # Тип отражения
                                   'reflection_scale': [0.3, 0.6, 1.5],  # Масштаб отражения
                                   'shadow_size': 0.0,  # Размер тени
                                   'is_area_of_interest': False,  # Флаг интересной зоны
                                   'position': position,  # Устанавливаем начальную позицию
                                   'materials': mats,  # Используемые материалы
                                   'model_scale': 0.15 * size,  # Масштаб модели
                                   'gravity_scale': 0.0,  # Гравитационный масштаб
                                   'velocity': (0.0, -16.0 * random.uniform(0.8, 1.2), 0.0)  # Начальная скорость
                               })
        self.owner = None

        self.fallTimer = ba.Timer(0.01, self.check_height, repeat=True)  # Таймер для проверки высоты

    def check_height(self):
        try:
            if self.node.position[1] >= 0.2:  # Проверяем высоту падения
                return
        except:
            pass
        self.fallTimer = None  # Останавливаем таймер
        self.handlemessage(ba.OutOfBoundsMessage())  # Обрабатываем сообщение об выходе за границы

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):  # Обработка сообщения о смерти
            self.node.delete()  # Удаляем узел

        elif isinstance(msg, ba.OutOfBoundsMessage):  # Обработка сообщения о выходе за границы
            activity = self.getactivity()
            # Проверяем возможность возрождения и флаг спавна капель дождя
            if self.respawn and hasattr(activity, 'spawn_raindrops') and not activity.spawn_raindrops:
                self.node.position = self._spawn_pos  # Устанавливаем позицию возрождения
                self.fallTimer = ba.Timer(0.01, self.check_height, repeat=True)  # Запускаем таймер проверки высоты
            else:
                self.handlemessage(ba.DieMessage())  # Иначе обрабатываем сообщение о смерти

        else:
            super().handlemessage(msg)  # Передаем сообщение выше


class Snowflake(ba.Actor):

    def __init__(self,
                 position: Sequence[float] = (0.0, 0.0, 0.0),
                 size: float = 1.0,
                 respawn = False):

        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты
        activity = self.getactivity()  # Получаем текущую активность

        # Импортируем материал для голограммы
        from actors.hologram import getHologramMaterial
        mats = [getHologramMaterial()]

        self._spawn_pos = position  # Устанавливаем позицию возрождения
        self.respawn = respawn  # Устанавливаем флаг возрождения
        # Создаем узел для объекта Snowflake
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('frostyPelvis'),  # Модель объекта
                                   'color_texture': ba.gettexture('white'),  # Белая текстура
                                   'body': 'sphere',  # Тип тела
                                   'reflection': 'soft',  # Тип отражения
                                   'reflection_scale': [0.1, 0.1, 0.3],  # Масштаб отражения
                                   'shadow_size': 0.0,  # Размер тени
                                   'is_area_of_interest': False,  # Флаг интересной зоны
                                   'position': position,  # Устанавливаем начальную позицию
                                   'velocity': (0.0, -3.6 * random.uniform(0.8, 1.2), 0.0),  # Начальная скорость
                                   'materials': mats,  # Используемые материалы
                                   'body_scale': 0.03 * size * 0.5,  # Масштаб тела
                                   'model_scale': 0.15 * size * 0.5,  # Масштаб модели
                                   'gravity_scale': 0.0  # Гравитационный масштаб
                               })
        self.owner = None

        self.fallTimer = ba.Timer(0.01, self.check_height, repeat=True)  # Таймер для проверки высоты

    def check_height(self):
        try:
            if self.node.position[1] >= 0.5:  # Проверяем высоту падения
                return
        except:
            pass
        self.fallTimer = None  # Останавливаем таймер
        self.handlemessage(ba.OutOfBoundsMessage())  # Обрабатываем сообщение об выходе за границы

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):  # Обработка сообщения о смерти
            self.node.delete()  # Удаляем узел

        elif isinstance(msg, ba.OutOfBoundsMessage):  # Обработка сообщения о выходе за границы
            activity = self.getactivity()
            # Проверяем возможность возрождения и флаг спавна снежинок
            if self.respawn and hasattr(activity, 'spawn_snowflakes') and not activity.spawn_snowflakes:
                self.node.position = self._spawn_pos  # Устанавливаем позицию возрождения
                self.fallTimer = ba.Timer(0.01, self.check_height, repeat=True)  # Запускаем таймер проверки высоты
            else:
                self.handlemessage(ba.DieMessage())  # Иначе обрабатываем сообщение о смерти

        else:
            super().handlemessage(msg)  # Передаем сообщение выше


class SmokeRing(ba.Actor):

    def __init__(self,
                 type: str = 'gray',
                 position: Sequence[float] = (0.0, 0.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты
        activity = self.getactivity()  # Получаем текущую активность

        radius = random.uniform(0.95, 1.05) * 0.5  # Случайный радиус кольца
        time_interval = 2.25  # Временной интервал анимации
        radius = random.uniform(0.9, 1.1) * radius  # Случайный радиус
        if type == 'gray':
            color = (0.7, 0.7, 0.7)  # Серый цвет
        elif type == 'white':
            color = (1.0, 1.0, 1.0)  # Белый цвет
        elif type == 'black':
            color = (0.0, 0.0, 0.0)  # Черный цвет
        # Создаем узел для объекта SmokeRing
        self.node = ba.newnode('locator',
                               attrs={
                                   'shape': 'circleOutline',  # Форма кольца
                                   'position': position,  # Устанавливаем начальную позицию
                                   'color': color,  # Устанавливаем цвет
                                   'size': (radius, radius, radius),  # Размер кольца
                                   'opacity': 0.8,  # Прозрачность
                                   'drawShadow': False,  # Не рисуем тень
                                   'additive': False  # Не добавляем
                               })
        # Анимируем размер кольца
        ba.animate_array(self.node, 'size', 3, {0.0: (radius, radius, radius), time_interval: (3.0 * radius, 3.0 * radius, 3.0 * radius)})
        # Анимируем движение кольца
        ba.animate_array(self.node, 'position', 3, {0.0: (position[0], position[1], position[2]), 0.5 * time_interval: (position[0], position[1] + 0.6, position[2]), time_interval: (position[0], position[1] + random.uniform(0.8, 1.1) * 4.5, position[2])})
        ba.timer(time_interval, ba.Call(self.handlemessage, ba.DieMessage()))  # Таймер для удаления

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):  # Обработка сообщения о смерти
            self.node.delete()  # Удаляем узел

        elif isinstance(msg, ba.OutOfBoundsMessage):  # Обработка сообщения о выходе за границы
            self.handlemessage(ba.DieMessage())  # Обрабатываем сообщение о смерти

        else:
            return None  # Возвращаем ничего
