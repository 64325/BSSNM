# ba_meta require api 7

from future import annotations
from typing import TYPE_CHECKING

import time, random

import _ba, ba
from ba import _gameactivity
from ba import _teamgame

from actors.particle_holograms import Raindrop, Snowflake

# Сохраняем ссылку на оригинальную функцию on_begin
old_on_begin = _gameactivity.GameActivity.on_begin

# Переопределяем функцию on_begin, которая вызывается при начале игры
def on_begin(self):
    # Вызываем оригинальную функцию on_begin для сохранения стандартного поведения игры
    old_on_begin(self)

    # Инициализация переменных для дождя и снега
    self.raining = False
    self.snowing = False

    # Запускаем случайные интервалы для дождя и снега
    self._add_random_rain_interval()
    self._add_random_snow_interval()


# Функция, устанавливающая случайные интервалы для дождя
def _add_random_rain_interval(self):
    # Выбираем случайное время для начала дождя (от 30 до 1500 секунд)
    rain_time = random.uniform(30.0, 1500.0) / 3.0
    # Выбираем случайный интервал между дождями (от 50 до 300 секунд)
    rain_interval = random.uniform(50.0, 300.0) / 3.0
    # Запускаем таймер для начала дождя
    ba.timer(rain_time, self._start_rain)
    # Запускаем таймер для окончания дождя
    ba.timer(rain_time + rain_interval, self._stop_rain)
    # Запускаем таймер для следующего интервала дождя
    ba.timer(rain_time + rain_interval + 20.0 / 3.0, self._add_random_rain_interval)


# Функция, запускающая дождь
def _start_rain(self):
    # Получаем границы карты
    bounds = self.map.defs.boxes['map_bounds']
    # Вычисляем размер карты
    map_size = bounds[6] * bounds[8]

    # Устанавливаем флаг, что дождь идет
    self.raining = True
    # Включаем создание капель дождя
    self.spawn_raindrops = True
    # Ставим таймер на 3 секунды, чтобы остановить создание капель дождя
    self.stopSpawnTimer = ba.Timer(3.0, self.stop_spawn)
    # Ставим таймер для создания капель дождя с определенным интервалом
    self.rainTimer = ba.Timer(3.0 / map_size * random.uniform(1.0, 1.0) / 3.0, self._rain, repeat=True)


# Функция, останавливающая дождь
def _stop_rain(self):
    # Останавливаем таймер создания капель дождя
    self.rainTimer = None
    # Устанавливаем флаг, что дождь не идет
    self.raining = False
    # Включаем создание капель дождя (для следующего раза)
    self.spawn_raindrops = True
    # Останавливаем таймер, останавливающий создание капель дождя
    self.stopSpawnTimer = None
# Функция, создающая одну каплю дождя
def _rain(self):
    # Если создание капель дождя остановлено, выходим из функции
    if not self.spawn_raindrops:
        return

    # Получаем границы карты
    bounds = self.map.defs.boxes['map_bounds']
    # Выбираем случайную позицию для капли дождя
    pos = (random.uniform(bounds[0] - 0.5 * bounds[6], bounds[0] + 0.5 * bounds[6]), bounds[1] + 0.4 * bounds[7], random.uniform(bounds[2] - 0.5 * bounds[8], bounds[2] + 0.5 * bounds[8]))
    # Создаем каплю дождя
    raindrop = Raindrop(position=pos, respawn=True).autoretain()
    # Изменяем параметры капли дождя
    raindrop.node.reflection_scale = [1.0, 1.0, 1.2]
    raindrop.node.model_scale = 0.8 * raindrop.node.model_scale
    raindrop.node.velocity = (0.0, -19.0 * random.uniform(0.8, 1.0), 0.0)


# Функция, устанавливающая случайные интервалы для снега
def _add_random_snow_interval(self):
    # Выбираем случайное время для начала снега (от 30 до 1500 секунд)
    snow_time = random.uniform(30.0, 1500.0) / 3.0
    # Выбираем случайный интервал между снегопадами (от 50 до 300 секунд)
    snow_interval = random.uniform(50.0, 300.0) / 3.0
    # Запускаем таймер для начала снега
    ba.timer(snow_time, self._start_snow)
    # Запускаем таймер для окончания снега
    ba.timer(snow_time + snow_interval, self._stop_snow)
    # Запускаем таймер для следующего интервала снега
    ba.timer(snow_time + snow_interval + 20.0 / 3.0, self._add_random_snow_interval)


# Функция, запускающая снегопад
def _start_snow(self):
    # Получаем границы карты
    bounds = self.map.defs.boxes['map_bounds']
    # Вычисляем размер карты
    map_size = bounds[6] * bounds[8]
    # Устанавливаем флаг, что снег идет
    self.snowing = True
    # Включаем создание снежинок
    self.spawn_snowflakes = True
    # Ставим таймер на 4 секунды, чтобы остановить создание снежинок
    self.stopSpawnTimer = ba.Timer(4.0, self.stop_spawn)
    # Ставим таймер для создания снежинок с определенным интервалом
    self.snowTimer = ba.Timer(30.0 / map_size * random.uniform(1.0, 1.0) / 3.0, self._snow, repeat=True)


# Функция, останавливающая снегопад
def _stop_snow(self):
    # Останавливаем таймер создания снежинок
    self.snowTimer = None
    # Устанавливаем флаг, что снег не идет
    self.snowing = False
    # Включаем создание снежинок (для следующего раза)
    self.spawn_snowflakes = True
    # Останавливаем таймер, останавливающий создание снежинок
    self.stopSpawnTimer = None


# Функция, создающая одну снежинку
def _snow(self):
    # Если создание снежинок остановлено, выходим из функции
    if not self.spawn_snowflakes:
        return

    # Получаем границы карты
    bounds = self.map.defs.boxes['map_bounds']
    # Выбираем случайную позицию для снежинки
    pos = (random.uniform(bounds[0] - 0.5 * bounds[6], bounds[0] + 0.5 * bounds[6]), bounds[1] + 0.4 * bounds[7], random.uniform(bounds[2] - 0.5 * bounds[8], bounds[2] + 0.5 * bounds[8]))
    # Создаем снежинку
    snowflake = Snowflake(position=pos, respawn=True).autoretain()
    # Изменяем параметры снежинки
    snowflake.node.reflection_scale = [0.6, 1.5, 2.0]
    snowflake.node.model_scale = 1.4 * snowflake.node.model_scale


# Функция, останавливающая создание капель дождя или снежинок
def stop_spawn(self):
    # Если дождь идет, останавливаем создание капель дождя
    if self.raining:
        self.spawn_raindrops = False
    # Если снег идет, останавливаем создание снежинок
    if self.snowing:
        self.spawn_snowflakes = False


#  Привязка новых функций к методам класса GameActivity
_gameactivity.GameActivity.on_begin = on_begin
_gameactivity.GameActivity._add_random_rain_interval = _add_random_rain_interval
_gameactivity.GameActivity._start_rain = _start_rain
_gameactivity.GameActivity._stop_rain = _stop_rain
_gameactivity.GameActivity._rain = _rain
_gameactivity.GameActivity._add_random_snow_interval = _add_random_snow_interval
_gameactivity.GameActivity._start_snow = _start_snow
_gameactivity.GameActivity._stop_snow = _stop_snow
_gameactivity.GameActivity._snow = _snow
_gameactivity.GameActivity.stop_spawn = stop_spawn
