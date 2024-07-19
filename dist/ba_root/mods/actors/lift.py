from __future__ import annotations  # Импорт для поддержки аннотаций в старых версиях Python

import random  # Импорт модуля random для генерации случайных чисел
from typing import TYPE_CHECKING, TypeVar  # Импорт для поддержки проверки типов во время выполнения

import ba  # Импорт основного модуля игры
from ba._messages import PlayerDiedMessage, StandMessage  # Импорт сообщений из внутреннего модуля ba._messages
from bastd.gameutils import SharedObjects  # Импорт утилит игры из внешнего модуля bastd.gameutils

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type  # Импорт типов для проверки во время выполнения

class Lift(ba.Actor):  # Определение класса Lift, наследующегося от класса ba.Actor

    def __init__(self,
                 size: float = 1.0,  # Размер лифта по умолчанию
                 position: Sequence[float] = (0.0, 1.0, 0.0),  # Позиция лифта по умолчанию
                 color: Sequence[float] = (1.0, 1.0, 0.0),  # Цвет лифта по умолчанию
                 materials: Sequence[ba.Material] = None):  # Материалы лифта
        super().__init__()  # Вызов конструктора родительского класса
        shared = SharedObjects.get()  # Получение общих объектов игры
        activity = self.getactivity()  # Получение активности, к которой принадлежит объект
        from bastd.actor.bomb import BombFactory  # Импорт фабрики бомб из внешнего модуля
        factory = BombFactory.get()  # Получение экземпляра фабрики бомб

        tnt_mat = factory.bomb_material  # Получение материала для бомбы
        tnt_mat.add_actions(actions=(('modify_part_collision',
                                      'friction', 1.5)))  # Настройка действий для материала бомбы

        from actors.hologram import getHologramMaterial, getRegionMaterial  # Импорт методов получения материалов
        hmats = [getHologramMaterial()]  # Получение голограммного материала
        rmats = (getRegionMaterial(), shared.footing_material,
                 shared.object_material)  # Получение региональных материалов

        self.node_scale = 2.4 * size  # Масштабирование узла лифта
        self.region_scale = size  # Масштабирование региона лифта
        self.node = ba.newnode('prop',  # Создание новой ноды типа 'prop'
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('flagStand'),  # Установка модели для ноды
                                   'color_texture': ba.gettexture('puckColor'),  # Установка текстуры цвета для ноды
                                   'body': 'crate',  # Тип тела ноды
                                   'body_scale': 0.01,  # Масштабирование тела ноды
                                   'model_scale': self.node_scale,  # Установка масштаба модели ноды
                                   'reflection': 'soft',  # Тип отражения для ноды
                                   'reflection_scale': [0.8, 0.8, 0.8],  # Установка коэффициентов отражения для ноды
                                   'shadow_size': 0.0,  # Размер тени ноды
                                   'is_area_of_interest': False,  # Является ли областью интереса
                                   'position': position,  # Установка позиции ноды
                                   'materials': hmats,  # Установка материалов ноды
                                   'gravity_scale': 0.0  # Установка коэффициента гравитации для ноды
                               })
        self.node.handlemessage('set_q', 1.0, 0.0, 0.0, 0.0)  # Отправка сообщения ноде

        self.region = ba.newnode('region',  # Создание новой ноды типа 'region'
                                 attrs={
                                     'position': position,  # Установка позиции региона
                                     'scale': (self.region_scale, self.region_scale * 0.05, self.region_scale),  # Установка масштаба региона
                                     'type': 'box',  # Тип региона
                                     'materials': rmats  # Установка материалов региона
                                 })

        self.region.connectattr('position', self.node, 'position')  # Установка соединения между регионом и нодой
        position_up = (position[0], position[1] + 4.0 * size, position[2])  # Позиция вверх относительно текущей позиции
        ba.animate_array(self.region, 'position', 3, {0: position, 2: position_up, 2.3: position_up, 4.3: position, 4.6: position}, loop=True)  # Анимация движения региона

        self.owner = None  # Инициализация владельца лифта как None

    def handlemessage(self, msg: Any) -> Any:  # Определение метода обработки сообщений
        if isinstance(msg, ba.DieMessage):  # Если сообщение - DieMessage
            self.node.delete()  # Удаление ноды
            self.region.delete()  # Удаление региона

        elif isinstance(msg, ba.OutOfBoundsMessage):  # Если сообщение - OutOfBoundsMessage
            pass  # Пропуск обработки

        elif isinstance(msg, ba.HitMessage):  # Если сообщение - HitMessage
            pass  # Пропуск обработки

        else:
            pass  # Пропуск обработки для других типов сообщений
