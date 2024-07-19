from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type

from bastd.actor.bomb import (BombFactory, SplatMessage, ExplodeMessage, ImpactMessage, ArmMessage, WarnMessage,
                             ExplodeHitMessage, Blast, Bomb, TNTSpawner)

class FreezeBomb(Bomb):

    # Ew; should try to clean this up later.
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 velocity: Sequence[float] = (0.0, 0.0, 0.0),
                 blast_radius: float = 2.0,
                 bomb_scale: float = 1.0,
                 source_player: ba.Player = None,
                 owner: ba.Node = None):
        """Create a new Bomb.
        """
        ba.Actor.__init__(self)  # Инициализация базового класса Actor.

        shared = SharedObjects.get()  # Получение общих объектов из SharedObjects.
        factory = BombFactory.get()  # Получение фабрики бомб из BombFactory.
        activity = self.getactivity()  # Получение текущей активности.

        # Тип бомбы устанавливается как 'ice'.
        self.bomb_type = 'ice'

        self._exploded = False  # Флаг взрыва устанавливается в False.
        self.scale = bomb_scale  # Установка масштаба бомбы.

        self.texture_sequence: Optional[ba.Node] = None  # Последовательность текстур (опционально).

        # Радиус взрыва устанавливается с учетом коэффициента.
        self.blast_radius = 1.45 * blast_radius * 1.5

        self._explode_callbacks: list[Callable[[Bomb, Blast], Any]] = []  # Список колбэков для взрыва.

        # Игрок, от которого исходит бомба.
        self._source_player = source_player

        # Типы столкновений по умолчанию устанавливаются как 'explosion' и 'ice' (subtype).
        self.hit_type = 'explosion'
        self.hit_subtype = self.bomb_type

        # Владелец ноды устанавливается.
        self.owner = owner

        # Материалы для ноды, включая специальный материал для замораживания.
        materials: tuple[ba.Material, ...]
        materials = (factory.bomb_material, shared.footing_material,
                     shared.object_material)
        materials = materials + (factory.normal_sound_material, )
        freeze_material = ba.Material()
        freeze_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=('message', 'their_node', 'at_connect', ba.FreezeMessage()),
        )
        materials = materials + (freeze_material, )

        fuse_time = None  # Время горения фитиля не устанавливается.

        # Создание ноды для бомбы с заданными атрибутами.
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'position': position,
                                   'velocity': velocity,
                                   'model': ba.getmodel('shield'),
                                   'model_scale': 0.26 * self.scale,
                                   'light_model': factory.tnt_model,
                                   'body': 'sphere',
                                   'body_scale': self.scale,
                                   'shadow_size': 0.5,
                                   'color_texture': ba.gettexture('bombColorIce'),
                                   'reflection': 'soft',
                                   'reflection_scale': [0.05, 0.4, 0.3],
                                   'materials': materials,
                                   'density': 1.0 / self.scale
                               })

        # Анимация изменения масштаба модели ноды бомбы.
        ba.animate(self.node, 'model_scale', {
            0: 0,
            0.2: 0.26 * 1.3 * self.scale,
            0.26: 0.26 * self.scale
        })
