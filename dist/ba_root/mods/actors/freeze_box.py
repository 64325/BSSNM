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

# Определяем новый класс FreezeBox, наследующийся от Bomb
class FreezeBox(Bomb):

    # Определяем конструктор класса
    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 velocity: Sequence[float] = (0.0, 0.0, 0.0),
                 blast_radius: float = 2.0,
                 bomb_scale: float = 1.0,
                 source_player: ba.Player = None,
                 owner: ba.Node = None):
        """Create a new Bomb.
        """
        ba.Actor.__init__(self)

        shared = SharedObjects.get()
        factory = BombFactory.get()
        activity = self.getactivity()
        
        # Устанавливаем тип бомбы
        self.bomb_type = 'ice'

        self._exploded = False
        self.scale = bomb_scale

        self.texture_sequence: Optional[ba.Node] = None

        # Устанавливаем радиус взрыва бомбы
        self.blast_radius = 1.45 * blast_radius * 1.5

        self._explode_callbacks: list[Callable[[Bomb, Blast], Any]] = []

        # Игрок, создавший бомбу
        self._source_player = source_player

        # Тип столкновения и подтип бомбы
        self.hit_type = 'explosion'
        self.hit_subtype = self.bomb_type

        # Узел, создавший бомбу
        self.owner = owner

        # Материалы, связанные с бомбой
        materials: tuple[ba.Material, ...]
        materials = (factory.bomb_material, shared.footing_material,
                     shared.object_material)
        materials = materials + (factory.normal_sound_material, )
        freeze_material = ba.Material()

        # Добавляем действие замораживания игроков при столкновении с материалом бомбы
        freeze_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=('message', 'their_node', 'at_connect', ba.FreezeMessage()),
        )
        materials = materials + (freeze_material, )

        fuse_time = None

        # Создаем узел для бомбы
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'position': position,
                                   'velocity': velocity,
                                   'model': factory.tnt_model,
                                   'light_model': factory.tnt_model,
                                   'body': 'crate',
                                   'body_scale': self.scale,
                                   'shadow_size': 0.5,
                                   'color_texture': ba.gettexture('bombColorIce'),
                                   'reflection': 'soft',
                                   'reflection_scale': [0.05, 0.4, 0.3],
                                   'materials': materials,
                                   'density': 1.0 / self.scale
                               })

        # Анимация масштабирования модели бомбы
        ba.animate(self.node, 'model_scale', {
            0: 0,
            0.2: 1.3 * self.scale,
            0.26: self.scale
        })

# Определяем класс FreezeBoxSpawner, наследующийся от TNTSpawner
class FreezeBoxSpawner(TNTSpawner):

    # Метод для обновления состояния спавнера
    def _update(self) -> None:
        tnt_alive = self._tnt is not None and self._tnt.node
        if not tnt_alive:
            # Переспауним, если прошло достаточно времени
            if self._tnt is None or self._wait_time >= self._respawn_time:
                self._tnt = FreezeBox(position=self._position)
                self._wait_time = 0.0
            else:
                self._wait_time += 1.1
