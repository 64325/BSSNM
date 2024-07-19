# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING

import time, random

import _ba, ba
from bastd.actor import spaz
from ModData.strings import *

from bastd.actor.spazfactory import SpazFactory

# Сохраняем оригинальный метод handlemessage из Spaz для использования позже
old_handlemessage = spaz.Spaz.handlemessage

# Новая реализация метода handlemessage для класса Spaz
def new_handlemessage(self, msg: Any) -> Any:

    # Если сообщение является сообщением о попадании (HitMessage)
    if isinstance(msg, ba.HitMessage):
        # Импортируем PopupText для отображения текста на экране
        from bastd.actor.popuptext import PopupText

        # Если узел (node) спаза не существует, возвращаем None
        if not self.node:
            return None
        # Если спаз неуязвим, проигрываем звук блокировки и завершаем обработку
        if self.node.invincible:
            ba.playsound(SpazFactory.get().block_sound,
                         1.0,
                         position=self.node.position)
            return True

        # Если спаз недавно был атакован, не считаем это как новое попадание
        local_time = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(local_time, int)
        if (self._last_hit_time is None
                or local_time - self._last_hit_time > 1000):
            self._num_times_hit += 1
            self._last_hit_time = local_time

        # Масштабируем урон и скорость от попадания
        mag = msg.magnitude * self.impact_scale
        velocity_mag = msg.velocity_magnitude * self.impact_scale
        damage_scale = 0.22

        # Если у спаза есть щит, урон направляется на него
        if self.shield:
            if msg.flat_damage:
                damage = msg.flat_damage * self.impact_scale
            else:
                # Наносим спазу импульс, но не применяем его, чтобы только оценить урон.
                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1], msg.velocity[2], mag,
                    velocity_mag, msg.radius, 1, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
                damage = damage_scale * self.node.damage

            assert self.shield_hitpoints is not None
            self.shield_hitpoints -= int(damage)
            self.shield.hurt = (
                1.0 -
                float(self.shield_hitpoints) / self.shield_hitpoints_max)

            # Если у щита закончились очки прочности, удаляем его
            max_spillover = SpazFactory.get().max_shield_spillover_damage
            if self.shield_hitpoints <= 0:
                self.shield.delete()
                self.shield = None
                ba.playsound(SpazFactory.get().shield_down_sound,
                             1.0,
                             position=self.node.position)

                # Выводим искры при уничтожении щита
                npos = self.node.position
                ba.emitfx(position=(npos[0], npos[1] + 0.9, npos[2]),
                          velocity=self.node.velocity,
                          count=random.randrange(20, 30),
                          scale=1.0,
                          spread=0.6,
                          chunk_type='spark')

            else:
                ba.playsound(SpazFactory.get().shield_hit_sound,
                             0.5,
                             position=self.node.position)

            # Выводим искры при попадании по щиту
            assert msg.force_direction is not None
            ba.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 1.0,
                                msg.force_direction[1] * 1.0,
                                msg.force_direction[2] * 1.0),
                      count=min(30, 5 + int(damage * 0.005)),
                      scale=0.5,
                      spread=0.3,
                      chunk_type='spark')

            # Если урон превышает порог разлива, передаем оставшийся урон спазу
            if self.shield_hitpoints <= -max_spillover:
                leftover_damage = -max_spillover - self.shield_hitpoints
                shield_leftover_ratio = leftover_damage / damage

                # Уменьшаем магнитуды, применяемые к спазу, соответственно
                mag *= shield_leftover_ratio
                velocity_mag *= shield_leftover_ratio
            else:
                return True  # Успешное блокирование урона щитом

        else:
            shield_leftover_ratio = 1.0

        # Если урон плоский, применяем его с учетом масштабирования и оставшегося урона щита
        if msg.flat_damage:
            damage = int(msg.flat_damage * self.impact_scale *
                         shield_leftover_ratio)
        else:
            # Наносим спазу импульс и получаем полученный урон
            if not self.protection:
                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1], msg.velocity[2], mag,
                    velocity_mag, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
            else:
                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1], msg.velocity[2], mag,
                    velocity_mag, msg.radius, 1, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])

            damage = int(damage_scale * self.node.damage)

        # Воспроизводим звук удара
        self.node.handlemessage('hurt_sound')

        # Воспроизводим звук удара кулаком в зависимости от урона
        if msg.hit_type == 'punch':
            self.on_punched(damage)

            # Если урон значительный, показываем его на экране
            if damage > 350:
                assert msg.force_direction is not None
                ba.show_damage_count('-' + str(int(damage / 10)) + '%',
                                     msg.pos, msg.force_direction)

            # Воспроизводим звук супер-удара с перчатками
            if msg.hit_subtype == 'super_punch':
                ba.playsound(SpazFactory.get().punch_sound_stronger,
                             1.0,
                             position=self.node.position)
            if damage > 500:
                sounds = SpazFactory.get().punch_sound_strong
                sound = sounds[random.randrange(len(sounds))]
            else:
                sound = SpazFactory.get().punch_sound
            ba.playsound(sound, 1.0, position=self.node.position)

            # Если урон больше 999, выводим сообщение "FATALITY!!!" и добавляем спецэффекты
            if damage > 999:
                activity = ba.getactivity()
                if not hasattr(activity, 'fatality_released'):
                    activity.fatality_released = []
                activity.fatality_released.append(time.time())
                i = len(activity.fatality_released) - 1
                while i >= 1 and activity.fatality_released[i] - activity.fatality_released[i - 1] <= 8.0:
                    i -= 1
                recent_fatalities = len(activity.fatality_released) - 1 - i
                fatality_colors = [
                    (1.0, 0.2, 0.2),
                    (1.0, 0.4, 0.4),
                    (1.0, 0.7, 0.4),
                    (1.0, 1.0, 0.4),
                    (0.7, 1.0, 0.4),
                    (0.6, 1.0, 0.6),
                    (0.8, 1.0, 0.9),
                    (0.8, 1.0, 1.0),
                    (0.6, 0.8, 1.0),
                    (0.6, 0.6, 1.0),
                    (0.8, 0.6, 1.0),
                    (1.0, 0.4, 1.0),
                    (1.0, 0.2, 0.6)
                ]
                fatality_color = fatality_colors[min(len(fatality_colors) - 1, recent_fatalities)]
                
                # Выводим текст "FATALITY!!!" с заданным цветом и эффектами
                PopupText(
                    'FATALITY!!!',
                    color=fatality_color,
                    scale=2.0,
                    position=self.node.position).autoretain()

                # Анимируем изменение цвета фона
                if not hasattr(activity, 'current_tint'):
                    activity.current_tint = (activity.globalsnode.tint[0], activity.globalsnode.tint[1], activity.globalsnode.tint[2])
                ba.animate_array(activity.globalsnode, 'tint', 3, {0: activity.globalsnode.tint, 0.15: (0.0, 0.0, 0.0), 0.45: activity.current_tint})

                # Выводим искры и эффекты при супер-ударе
                ba.emitfx(
                    position=msg.pos,
                    chunk_type='spark',
                    velocity=(msg.force_direction[0] * 1.3,
                              msg.force_direction[1] * 1.3 + 5.0,
                              msg.force_direction[2] * 1.3),
                    count=45,
                    scale=1.0,
                    spread=1.0)
            else:
                # Выводим мелкие частицы при ударе
                assert msg.force_direction is not None
                ba.emitfx(position=msg.pos,
                          velocity=(msg.force_direction[0] * 0.5,
                                    msg.force_direction[1] * 0.5,
                                    msg.force_direction[2] * 0.5),
                          count=min(10, 1 + int(damage * 0.0025)),
                          scale=0.3,
                          spread=0.03)

                # Выводим частицы при ударе (sweat)
                ba.emitfx(position=msg.pos,
                          chunk_type='sweat',
                          velocity=(msg.force_direction[0] * 1.3,
                                    msg.force_direction[1] * 1.3 + 5.0,
                                    msg.force_direction[2] * 1.3),
                          count=min(30, 1 + int(damage * 0.04)),
                          scale=0.9,
                          spread=0.28)

            # Мгновенная вспышка света при ударе
            hurtiness = damage * 0.003
            punchpos = (msg.pos[0] + msg.force_direction[0] * 0.02,
                        msg.pos[1] + msg.force_direction[1] * 0.02,
                        msg.pos[2] + msg.force_direction[2] * 0.02)
            source_player = msg.get_source_player(ba.Player)
            if source_player != None and source_player.actor and hasattr(source_player.actor, 'punchcolor') and len(source_player.actor.punchcolor) != 0:
                flash_color = source_player.actor.punchcolor
            else:
                flash_color = (1.0, 0.8, 0.4)
            light = ba.newnode(
                'light',
                attrs={
                    'position': punchpos,
                    'radius': 0.12 + hurtiness * 0.12,
                    'intensity': 0.3 * (1.0 + 1.0 * hurtiness),
                    'height_attenuated': False,
                    'color': flash_color
                })
            ba.timer(0.06, light.delete)

            flash = ba.newnode('flash',
                               attrs={
                                   'position': punchpos,
                                   'size': 0.17 + 0.17 * hurtiness,
                                   'color': flash_color
                               })
            ba.timer(0.06, flash.delete)

        # Если сообщение о типе попадания "impact", выводим эффекты удара
        if msg.hit_type == 'impact':
            assert msg.force_direction is not None
            ba.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 2.0,
                                msg.force_direction[1] * 2.0,
                                msg.force_direction[2] * 2.0),
                      count=min(10, 1 + int(damage * 0.01)),
                      scale=0.4,
                      spread=0.1)

        # Если у спаза есть защита, просто завершаем обработку сообщения
        if self.protection:
            return None

        # Если у спаза остались хитпоинты, обрабатываем урон
        if self.hitpoints > 0:

            # Снижаем урон от ударов, если он не убивает спаз
            if msg.hit_type == 'impact' and damage > self.hitpoints:
                newdamage = max(damage - 200, self.hitpoints - 10)
                damage = newdamage

            # Уменьшаем количество хитпоинтов спаза и обновляем его состояние hurt
            self.node.handlemessage('flash')

            # Если спаз держит что-то, он выпускает это
            if damage > 0.0 and self.node.hold_node:
                self.node.hold_node = None

            # Если спаз не бессмертен, уменьшаем его хитпоинты на урон
            if not self.immortal:
                self.hitpoints -= damage
            self.node.hurt = 1.0 - float(
                self.hitpoints) / self.hitpoints_max

            # Если спаз проклят, любой урон взрывает его
            if self._cursed and damage > 0 and not self.godmode:
                ba.timer(
                    0.05,
                    ba.WeakCall(self.curse_explode,
                                msg.get_source_player(ba.Player)))

            # Если спаз заморожен, он разламывается, иначе умирает при достижении нулевых хитпоинтов
            if self.frozen and (damage > 200 or self.hitpoints <= 0):
                self.shatter()
            elif self.hitpoints <= 0:
                self.node.handlemessage(
                    ba.DieMessage(how=ba.DeathType.IMPACT))

        # Если спаз мертв, проверяем сглаженное значение урона и взрываем его, если оно слишком высоко
        if self.hitpoints <= 0:
            damage_avg = self.node.damage_smoothed * damage_scale
            if damage_avg > 1000:
                self.shatter()

    else:
        return old_handlemessage(self, msg)


# ba_meta export plugin
class punchEffects(ba.Plugin):
    def __init__(self):
        spaz.Spaz.handlemessage = new_handlemessage
