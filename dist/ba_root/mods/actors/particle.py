from __future__ import annotations  # Импорт для поддержки аннотаций в Python 3.7 и выше

import time
import random, math
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

from actors.cloud import Cloud
from actors.particle_holograms import Raindrop, Snowflake, SmokeRing

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type


class ParticleSpawner(ba.Actor):

    def __init__(self,
                 source_actor,
                 type = 'snow',  # Тип частиц по умолчанию - снег
                 size = 1.0,  # Размер частицы
                 time_interval = 0.5,  # Интервал времени между спаунами частиц
                 position = (0.0, 0.0, 0.0)):  # Позиция спауна частиц по умолчанию

        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        self.owner = source_actor.node  # Устанавливаем владельца частицы как узел исходного актора

        self.type = type  # Тип частиц
        self.size = max(0.1, min(10.0, size))  # Ограничиваем размер частицы от 0.1 до 10.0

        # Определяем параметры в зависимости от типа частицы
        if type == 'snowcloud' or type == 'raincloud':
            self.time_interval = 0.12  # Интервал времени для облака снега или дождя
            offset = (0.0, 2.5, 0.0)  # Смещение для позиции частиц
            self.count = 1  # Количество частиц
        elif type == 'ice' or type == 'snow' or type == 'slime' or type == 'metal' or type == 'rock' or type == 'splinter':
            self.time_interval = max(0.15, time_interval)  # Интервал времени для других типов частиц
            offset = (0.0, 0.0, 0.0)  # Смещение для позиции частиц
            self.count = max(1, int(2.0 / math.sqrt(time_interval)))  # Вычисляем количество частиц исходя из временного интервала
        else:
            self.time_interval = max(0.05, time_interval)  # Интервал времени для остальных типов частиц
            if type == 'spark':
                offset = (0.0, -0.4, 0.0)  # Смещение для позиции частиц
                self.count = 4  # Количество частиц
            else:
                offset = (0.0, 0.0, 0.0)  # Смещение для позиции частиц
                if type == 'sweat':
                    self.count = 4  # Количество частиц
                else:
                    self.count = 1  # Количество частиц

        # Уменьшаем интервал времени, если активирован замедленный режим
        try:
            activity = ba.getactivity()
            if activity.globalsnode.slow_motion:
                self.time_interval /= 3.0
        except:
            pass

        # Создаем узел для позиционирования частиц относительно исходного актора
        if source_actor and source_actor.node:
            self.node = ba.newnode('math',
                               owner=source_actor.node,
                               attrs={
                                   'input1': (offset[0], offset[1], offset[2]),
                                   'operation': 'add'
                               })
            source_actor.node.connectattr('position_center', self.node, 'input2')

        # Если тип частицы - облако снега или дождя, создаем соответствующий объект
        if type == 'snowcloud' or type == 'raincloud':
            from actors.cloud import Cloud
            self.cloud = Cloud()
            self.node.connectattr('output', self.cloud.node, 'position')

        # Запускаем таймер для спауна частиц
        self.spawnTimer = ba.Timer(self.time_interval, self._spawn, repeat=True)

    def _spawn(self):
        try:
            pos = self.node.output  # Получаем позицию спауна частиц
            count = self.count  # Получаем количество частиц

            # В зависимости от типа частицы, спауним соответствующие эффекты
            if self.type == 'ice':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=count,
                          scale=1.0 * self.size,
                          chunk_type='ice',
                          spread=0.1
                )
            elif self.type == 'snow':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=count,
                          scale=0.25 * self.size,
                          chunk_type='ice',
                          spread=0.3
                )
            elif self.type == 'slime':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=count,
                          scale=1.0 * self.size,
                          chunk_type='slime',
                          spread=0.1
                )
            elif self.type == 'spark':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=4 * count,
                          scale=1.0 * self.size,
                          chunk_type='spark',
                          spread=0.1
                )
            elif self.type == 'metal':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=count,
                          scale=0.8 * self.size,
                          chunk_type='metal',
                          spread=0.1
                )
            elif self.type == 'rock':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=count,
                          scale=1.2 * self.size,
                          chunk_type='rock',
                          spread=0.1
                )
            elif self.type == 'splinter':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=count,
                          scale=0.7 * self.size,
                          chunk_type='splinter',
                          spread=0.1
                )
            elif self.type == 'sweat':
                ba.emitfx(position=pos,
                          velocity=(0.0, 0.0, 0.0),
                          count=count,
                          scale=3.0 * self.size,
                          chunk_type='sweat',
                          spread=0.1
                )
            elif self.type == 'fairy':
                ba.emitfx(position=pos,
                          emit_type='fairydust')
                ba.emitfx(position=pos,
                          emit_type='fairydust')
            elif self.type == 'snowcloud':
                vel = self.owner.velocity
                snowflake = Snowflake(position=(pos[0] + random.uniform(-0.7, 0.7), pos[1] - 0.3, pos[2] + random.uniform(-0.7, 0.7)))
                snowflake.node.model_scale = 0.7 * snowflake.node.model_scale
                snowflake.node.velocity = (0.5 * vel[0], snowflake.node.velocity[1], 0.5 * vel[2])
            elif self.type == 'raincloud':
                vel = self.owner.velocity
                raindrop = Raindrop(position=(pos[0] + random.uniform(-0.5, 0.5), pos[1] - 0.3, pos[2] + random.uniform(-0.5, 0.5)))
                raindrop.node.model_scale = 0.7 * raindrop.node.model_scale
                raindrop.node.velocity = (0.5 * vel[0], raindrop.node.velocity[1], 0.5 * vel[2])
            elif self.type == 'smoke':
                smoke_ring = SmokeRing(position=(pos[0], pos[1], pos[2]))
            elif self.type == 'steam':
                smoke_ring = SmokeRing(type='white', position=(pos[0], pos[1], pos[2]))
            elif self.type == 'devil':
                smoke_ring = SmokeRing(type='black', position=(pos[0], pos[1], pos[2]))

        except:
            self.handlemessage(ba.DieMessage())

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            self.spawnTimer = None
            if self.type == 'snowcloud' or self.type == 'raincloud':
                self.cloud.handlemessage(ba.DieMessage())
            self.node.delete()
