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

class DeathBomb(Bomb):

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
        ba.Actor.__init__(self)

        shared = SharedObjects.get()
        factory = BombFactory.get()
        activity = self.getactivity()
        
        self.bomb_type = 'normal'

        self._exploded = False
        self.scale = bomb_scale

        self.texture_sequence: Optional[ba.Node] = None

        self.blast_radius = 1.45 * blast_radius * 1.5

        self._explode_callbacks: list[Callable[[Bomb, Blast], Any]] = []

        # The player this came from.
        self._source_player = source_player

        # By default our hit type/subtype is our own, but we pick up types of
        # whoever sets us off so we know what caused a chain reaction.
        # UPDATE (July 2020): not inheriting hit-types anymore; this causes
        # weird effects such as land-mines inheriting 'punch' hit types and
        # then not being able to destroy certain things they normally could,
        # etc. Inheriting owner/source-node from things that set us off
        # should be all we need I think...
        self.hit_type = 'explosion'
        self.hit_subtype = self.bomb_type

        # The node this came from.
        # FIXME: can we unify this and source_player?
        self.owner = owner

        # Adding footing-materials to things can screw up jumping and flying
        # since players carrying those things and thus touching footing
        # objects will think they're on solid ground.. perhaps we don't
        # wanna add this even in the tnt case?
        materials: tuple[ba.Material, ...]
        materials = (factory.bomb_material, shared.footing_material,
                     shared.object_material)
        materials = materials + (factory.normal_sound_material, )
        freeze_material = ba.Material()
        freeze_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=('message', 'their_node', 'at_connect', ba.DieMessage()),
        )
        materials = materials + (freeze_material, )

        fuse_time = None
        
        # Создаем новый узел (node) для объекта 'prop'
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
                                   'color_texture': ba.gettexture('powerupCurse'),
                                   'reflection': 'soft',
                                   'reflection_scale': [0.05, 0.4, 0.3],
                                   'materials': materials,
                                   'density': 1.0 / self.scale
                               })

        # Анимируем масштабирование модели узла (node)
        ba.animate(self.node, 'model_scale', {
            0: 0,
            0.2: 0.26 * 1.3 * self.scale,
            0.26: 0.26 * self.scale
        })
