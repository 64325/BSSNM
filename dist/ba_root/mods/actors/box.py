from __future__ import annotations  # Импорт для поддержки аннотаций в Python 3.7+

import random
from typing import TYPE_CHECKING, TypeVar

import ba
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Callable, List, Tuple, Type


class Box(ba.Actor):

    def __init__(self,
                 size: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 0.0),
                 materials: Sequence[ba.Material] = None):
        super().__init__()
        shared = SharedObjects.get()  # Получаем общие объекты из игры
        activity = self.getactivity()  # Получаем текущую активность игры
        from bastd.actor.bomb import BombFactory
        factory = BombFactory.get()  # Получаем фабрику бомб

        tnt_mat = factory.bomb_material  # Материал для взрывчатки
        tnt_mat.add_actions(actions=(('modify_part_collision',
                                      'friction', 1.5)))  # Добавляем действие к материалу

        mats = (tnt_mat, shared.footing_material,
                shared.object_material)  # Список материалов для узла объекта

        self._spawn_pos = (position[0], position[1], position[2])  # Позиция появления объекта
        self.scored = False  # Показатель, отмечающий, были ли набраны очки
        assert activity is not None  # Проверка наличия активности

        self.scale = 0.7 * size  # Масштаб объекта

        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('tnt'),  # Модель объекта
                                   'color_texture': ba.gettexture('bg'),  # Текстура цвета фона
                                   'body': 'crate',  # Тип тела
                                   'body_scale': self.scale,  # Масштаб тела
                                   'model_scale': self.scale,  # Масштаб модели
                                   'reflection': 'soft',  # Тип отражения
                                   'reflection_scale': color,  # Масштаб отражения
                                   'shadow_size': 0.0,  # Размер тени
                                   'is_area_of_interest': True,  # Флаг области интереса
                                   'position': self._spawn_pos,  # Позиция объекта
                                   'materials': mats,  # Материалы объекта
                                   'density': 1.0 / self.scale / self.scale  # Плотность объекта
                               })
        self.owner = None  # Владелец объекта

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):  # Обработка сообщения о смерти объекта
            self.node.delete()  # Удаляем узел объекта

        elif isinstance(msg, ba.OutOfBoundsMessage):  # Обработка сообщения о выходе за границы
            self.handlemessage(ba.DieMessage())  # Обрабатываем как сообщение о смерти

        elif isinstance(msg, ba.HitMessage):  # Обработка сообщения о попадании
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1],
                msg.force_direction[2])  # Передаем сообщение узлу объекта

        else:
            super().handlemessage(msg)  # Обработка остальных сообщений через родительский метод
