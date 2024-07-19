# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING

import time
import os
import random

import _ba, ba
from ba._lobby import Chooser

# Сохраняем оригинальные методы для последующего вызова
old__del__ = Chooser.__del__
old__init__ = Chooser.__init__

# Импортируем необходимые утилиты для анимации и локализации строк
from ba._gameutils import animate, animate_array
from ba._language import Lstr

# Новый метод для удаления объекта
def new__del__(self) -> None:
    old__del__(self)
    if self._text_node2:
        self._text_node2.delete()

# Новый конструктор с добавлением текстового узла
def new__init__(self, vpos: float, sessionplayer: _ba.SessionPlayer,
                 lobby: 'Lobby') -> None:
    self._text_node2: ba.Node | None = None
    self._text_node2 = _ba.newnode('text',
                                      owner=None,
                                      attrs={
                                          'maxwidth': 160,
                                          'shadow': 0.5,
                                          'vr_depth': -20,
                                          'h_align': 'left',
                                          'v_align': 'center',
                                          'v_attach': 'top'
                                      })
    old__init__(self, vpos, sessionplayer, lobby)
    animate(self._text_node2, 'scale', {0: 0, 0.1: 0.7})
    self._text_node.connectattr('color', self._text_node2, 'color')
    self._update_position()

# Новый метод для обновления позиции элементов
def new_update_position(self) -> None:
    if True:
        """Update this chooser's position."""

        assert self._text_node
        spacing = 350
        sessionteams = self.lobby.sessionteams
        offs = (spacing * -0.5 * len(sessionteams) +
                spacing * self._selected_team_index + 250)
        if len(sessionteams) > 1:
            offs -= 35
        animate_array(self._text_node, 'position', 2, {
            0: self._text_node.position,
            0.1: (-100 + offs, self._vpos + 23 + 7)
        })
        animate_array(self._text_node2, 'position', 2, {
            #0: self._text_node2.position,
            0: (-100 + offs, self._vpos + 23 - 20 + 7),
            0.1: (-100 + offs, self._vpos + 23 - 20 + 7)
        })
        animate_array(self.icon, 'position', 2, {
            0: self.icon.position,
            0.1: (-130 + offs, self._vpos + 22)
        })

# Новый метод для обновления текста
def new_update_text(self) -> None:
    if True:
        assert self._text_node is not None
        if self._ready:

            # Once we're ready, we've saved the name, so lets ask the system
            # for it so we get appended numbers and stuff.
            text = Lstr(value=self._sessionplayer.getname(full=True))
            text = Lstr(value='${A} (${B})',
                        subs=[('${A}', text),
                              ('${B}', Lstr(resource='readyText'))])
            text2 = Lstr(value=self._character_names[self._character_index])
        else:
            text = Lstr(value=self._getname(full=True))
            text2 = Lstr(value=self._character_names[self._character_index])

        can_switch_teams = len(self.lobby.sessionteams) > 1

        # Flash as we're coming in.
        fin_color = _ba.safecolor(self.get_color()) + (1, )
        if not self._inited:
            animate_array(self._text_node, 'color', 4, {
                0.15: fin_color,
                0.25: (2, 2, 2, 1),
                0.35: fin_color
            })
            animate_array(self._text_node2, 'color', 4, {
                0.15: fin_color,
                0.25: (2, 2, 2, 1),
                0.35: fin_color
            })
        else:

            # Blend if we're in teams mode; switch instantly otherwise.
            if can_switch_teams:
                animate_array(self._text_node, 'color', 4, {
                    0: self._text_node.color,
                    0.1: fin_color
                })
                animate_array(self._text_node2, 'color', 4, {
                    0: self._text_node.color,
                    0.1: fin_color
                })
            else:
                self._text_node.color = fin_color
                self._text_node2.color = fin_color

        self._text_node.text = text
        self._text_node2.text = text2

# Заменяем оригинальные методы на новые
Chooser.__del__ = new__del__
Chooser.__init__ = new__init__
Chooser._update_position = new_update_position
Chooser._update_text = new_update_text

# ba_meta export plugin
class CharacterChooserPlugin(ba.Plugin):
    def __init__(self):
        pass
