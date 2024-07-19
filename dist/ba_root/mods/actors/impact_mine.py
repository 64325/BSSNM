from __future__ import annotations  # Импорт для поддержки аннотаций в старых версиях Python

import random  # Импорт модуля random для генерации случайных чисел
from typing import TYPE_CHECKING, TypeVar  # Импорт для поддержки проверки типов во время выполнения

import ba  # Импорт основного модуля игры
from ba._messages import PlayerDiedMessage, StandMessage  # Импорт сообщений из внутреннего модуля ba._messages
from bastd.gameutils import SharedObjects  # Импорт утилит игры из внешнего модуля bastd.gameutils

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type  # Импорт типов для проверки во время выполнения

from bastd.actor.bomb import (BombFactory, SplatMessage, ExplodeMessage, ImpactMessage, ArmMessage, WarnMessage,
                             ExplodeHitMessage, Blast, Bomb, TNTSpawner)  # Импорт различных классов и сообщений из модуля bomb

class ImpactMine(Bomb):  # Определение класса ImpactMine, наследующегося от класса Bomb

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),  # Позиция мины по умолчанию
                 velocity: Sequence[float] = (0.0, 0.0, 0.0),  # Скорость мины по умолчанию
                 blast_radius: float = 2.0,  # Радиус взрыва мины
                 bomb_scale: float = 1.0,  # Масштаб мины
                 source_player: ba.Player = None,  # Игрок, инициировавший взрыв
                 owner: ba.Node = None):  # Владелец мины
        """Create a new Bomb.
        """
        super().__init__(position, velocity, 'impact', 4.0 * blast_radius * bomb_scale, 1.5 * bomb_scale)
        self.node.gravity_scale = 0  # Установка коэффициента гравитации для ноды мины
        self.node.color_texture = ba.gettexture('empty')  # Установка текстуры цвета для ноды мины
        self.node.reflection_scale = [0.4, 0.4, 0.4]  # Установка коэффициентов отражения для ноды мины

    def arm(self):
        return  # Пустой метод arm(), не требующий реализации
