# ba_meta require api 7

# Импорт необходимых модулей и библиотек
from __future__ import annotations
from typing import TYPE_CHECKING

import _ba, ba

# Импорт данных сессии, игровой активности и игроков
from ModData import session_data
from ModData import gameactivity_data
from ModData import playerspaz_data

# ba_meta export plugin
# Определение класса плагина ModData
class ModData(ba.Plugin):
    # Инициализация класса
    def __init__(self):
        pass
