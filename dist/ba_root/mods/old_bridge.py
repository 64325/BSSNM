# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING
from bastd.maps import *  # Импортируем необходимые модули и классы

import ba
import _ba
from ba import _map
import random

if TYPE_CHECKING:
    from typing import Any, List, Dict

class new_defs():
    points = {}
    boxes = {}

class OldBridge(ba.Map):
    """An old beautiful long bridge."""
    
    # Используем новую структуру для точек и областей
    defs = new_defs()
    from bastd.mapdata import bridgit
    from copy import deepcopy
    defs.points = deepcopy(bridgit.points)
    defs.boxes = deepcopy(bridgit.boxes)

    # Задаем точки спауна для FFA режима
    defs.points['ffa_spawn1'] = (-8.0, 3.6, -2.3) + (2.0, 0.4, 0.2)
    defs.points['ffa_spawn2'] = (0.0, 3.6, -2.3) + (2.0, 0.4, 0.2)
    defs.points['ffa_spawn3'] = (8.0, 3.6, -2.3) + (2.0, 0.4, 0.2)
    
    # Задаем границы карты
    defs.boxes['map_bounds'] = (-0.1916036665, 7.481446847, 8.0) + (0.0, 0.0, 0.0) + (48.0, 18.47258973, 45.0)
    defs.boxes['area_of_interest_bounds'] = defs.boxes['map_bounds']

    name = 'Old Bridge'  # Название карты
    dataname = 'bridgit'  # Имя данных карты

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        # Возвращаем допустимые типы игры для этой карты
        return ['melee', 'team_flag', 'keep_away']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        # Возвращаем имя текстуры предпросмотра карты
        return 'bridgitPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model_top': ba.getmodel('bridgitLevelTop'),  # Загружаем модель верха моста
            'model_bottom': ba.getmodel('bridgitLevelBottom'),  # Загружаем модель низа моста
            'model_bg': ba.getmodel('natureBackground'),  # Загружаем фоновую модель
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),  # Загружаем модель VR фона
            'collide_model': ba.getcollidemodel('bridgitLevelCollide'),  # Загружаем коллизионную модель
            'tex': ba.gettexture('bridgitLevelColor'),  # Загружаем текстуру цвета уровня моста
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),  # Загружаем текстуру фона
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),  # Загружаем коллизионную модель фона
            'railing_collide_model': ba.getcollidemodel('bridgitLevelRailingCollide'),  # Загружаем коллизионную модель перил моста
            'bg_material': ba.Material()  # Создаем материал для фона
        }
        data['bg_material'].add_actions(actions=('modify_part_collision', 'friction', 10.0))
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = None
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],  # Устанавливаем модель фона
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],  # Устанавливаем текстуру цвета фона
                'color': (0.9, 0.8, 0.75)  # Устанавливаем цвет фона
            })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['bg_vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['model_bg_tex']
                   })
        self.bg_collide = ba.newnode('terrain',
                                     attrs={
                                         'collide_model': self.preloaddata['collide_bg'],
                                         'materials': [
                                             shared.footing_material,
                                             self.preloaddata['bg_material'],
                                         ]
                                     })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2 * 1.1, 1.2 * 1.2, 1.2 * 1.3)
        gnode.ambient_color = (1.1, 1.2, 1.3)
        gnode.vignette_outer = (0.65, 0.6, 0.55)
        gnode.vignette_inner = (0.9, 0.9, 0.93)

        self.nodes = []

        from actors.hologram import Hologram, getRegionMaterial
        shared = SharedObjects.get()
        activity = ba.getactivity()

        # Добавляем голограммы и регионы
        self.nodes.append(
            Hologram(position=(-9.0, 0.8, -2.0),
                     orientation=(0.0, 1.0, 0.0, 2.0),
                     size=0.8,
                     model='bridgitLevelBottom',
                     texture='bridgitLevelColor',
                     color=(-2.0, -3.0, -3.0))
        )
        self.nodes.append(
            Hologram(position=(9.0, 0.8, -2.0),
                     orientation=(0.0, 1.0, 0.0, 2.0),
                     size=0.8,
                     model='bridgitLevelBottom',
                     texture='bridgitLevelColor',
                     color=(-2.0, -3.0, -3.0))
        )
        self.nodes.append( Hologram(position=(-5.0, -8.0, 12.0),
                     orientation=(0.0, 1.0, 0.0, 0.0), size=3.0,
                     model='doomShroomLevel', texture='doomShroomLevelColor',
                     color=(-1.5, -0.2, 0.1))
        )
        for i in range(11):
            self.nodes.append( Hologram(position=(-13.2 + 2.64 * i, 2.0, -1.3),
                     orientation=(0.0, 1.0, 0.0, 0.0), size=0.16,
                     model='rampageLevel', texture='rampageLevelColor',
                     color=(-2.8, -1.9, -3.0))
            )
        for i in range(11):
            self.nodes.append( Hologram(position=(-13.2 + 2.64 * i, 2.0, -1.9),
                     orientation=(0.0, 1.0, 0.0, 0.0), size=0.16,
                     model='rampageLevel', texture='rampageLevelColor',
                     color=(-2.8, -1.9, -3.0))
            )
        maxtan = 0.15
        for i in range(11):
            x = -maxtan * (i - 5.0) / 11.0
            y = 1.0
            self.nodes.append( Hologram(position=(-12.8 + 2.56 * i, 3.2 + 100.0 * x * x, -2.9),
                     orientation=(x, y, 0.0, 90.0), size=1.6,
                     model='flagPole', texture='bonesColorMask',
                     color=(0.0, 0.5, 0.3))
            )
        for i in range(11):
            x = -maxtan * (i - 5.0) / 11.0
            y = 1.0
            self.nodes.append( Hologram(position=(-12.8 + 2.56 * i, 3.2 + 100.0 * x * x, -1.7),
                     orientation=(x, y, 0.0, 90.0), size=1.6,
                     model='flagPole', texture='bonesColorMask',
                     color=(0.0, 0.5, 0.3))
            )
        
        # Добавляем регионы
        self.nodes.append(
            ba.NodeActor(
                ba.newnode('region',
                           attrs={
                               'position': (0.0, 2.6, -2.3),
                               'scale': (29.0, 0.6, 1.4),
                               'type': 'box',
                               'materials': [getRegionMaterial(), shared.footing_material,
                                             shared.object_material]
                           })))
        self.nodes.append(
            ba.NodeActor(
                ba.newnode('region',
                           attrs={
                               'position': (0.0, 3.5, -3.0),
                               'scale': (29.0, 0.2, 0.2),
                               'type': 'box',
                               'materials': [getRegionMaterial(), shared.footing_material,
                                             shared.object_material]
                           })))
        self.nodes.append(
            ba.NodeActor(
                ba.newnode('region',
                           attrs={
                               'position': (0.0, 3.5, -1.6),
                               'scale': (29.0, 0.2, 0.2),
                               'type': 'box',
                               'materials': [getRegionMaterial(), shared.footing_material,
                                             shared.object_material]
                           })))

# ba_meta export plugin
class OldBridgePlugin(ba.Plugin):
    def __init__(self):
        _map.register_map(OldBridge)  # Регистрируем карту OldBridge в системе карт
