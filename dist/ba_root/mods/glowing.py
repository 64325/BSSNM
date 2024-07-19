# Copyright (c) 2020 Daniil Rakhov
#
# Разрешение на использование, изменение и распространение данного программного обеспечения,
# включая включение в него разрешено без ограничений, при условии,
# что вся копия этого уведомления об авторских правах и это разрешение
# остаются в неизменном виде во всех копиях или значительных частях программного обеспечения.
#
# ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ "КАК ЕСТЬ", БЕЗ ЛЮБЫХ ГАРАНТИЙ,
# ЯВНЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ, НО НЕ ОГРАНИЧИВАЯСЯ ГАРАНТИЯМИ
# ТОВАРНОГО СОСТОЯНИЯ, ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННОЙ ЦЕЛИ И НЕ НАРУШЕНИЯ.
# В НИКАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ЗА
# ЛЮБЫЕ ИСКИ, УЩЕРБ ИЛИ ДРУГИЕ ОБЯЗАТЕЛЬСТВА, ВОЗНИКШИЕ В РЕЗУЛЬТАТЕ,
# В СВЯЗИ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ ИЛИ ИСПОЛЬЗОВАНИЕМ ИЛИ ИНЫМИ ДЕЙСТВИЯМИ
# В ПРОГРАММНОМ ОБЕСПЕЧЕНИИ.

# ba_meta require api 7
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Callable

if TYPE_CHECKING:
    from ba._profile import get_player_profile_colors
    from ba._error import print_exception
    import _ba, ba

def __init__(self, 
      vpos: float, 
      sessionplayer: _ba.SessionPlayer,
      lobby: ba._lobby.Lobby) -> None:
    self._markers = ['"',"'","^","%",";","`"]
    self._glowing = {}
    self.__init___glowing(vpos, sessionplayer, lobby)
    
def get_glowing(self) -> Dict[str, List[float, float, int, int]]:
    # Функция для получения информации о "сияющих" профилях
    for profile_name in self._profilenames:
        for m in self._markers:
            if m in profile_name:
                s = profile_name.split(',')
                if len(s) > 3:
                    if s[0] != m:
                        s = [m, s[0].replace(m, '')] + s[1:]
                    result = []
                    for i, c in enumerate(s[1:5]):
                        try:
                            result.append(min(200000, max(float(c), -200000)) if i in range(2) else int(c))
                        except ValueError:
                            break
                    if len(result) == 4:    
                        self._glowing[m] = result
    return self._glowing

def update_from_profile(self) -> None:
    """Обновление персонажа и цветов на основе текущего профиля."""
    self._profilename = self._profilenames[self._profileindex]
    self.get_glowing()
    if self._profilename[0] in self._glowing:
        m = self._profilename[0]
        character = self._profiles[self._profilename]['character']

        if (character not in self._character_names
                and character in _ba.app.spaz_appearances):
            self._character_names.append(character)
        self._character_index = self._character_names.index(character)

        color_multiple = self._glowing[m][0]
        highlight_multiple = self._glowing[m][1]

        self._color, self._highlight = (get_player_profile_colors(
            self._profilename, profiles=self._profiles))
        
        if not (self._glowing[m][2] > 0):
            self._color = tuple([i * color_multiple for i in list(self._color)])
        else:
            self._color = list(self._color)
            val = max(self._color)
            
            for i, c in enumerate(self._color):
                if c == val:
                    self._color[i] *= color_multiple
            self._color = tuple(self._color)
                    
        if not (self._glowing[m][3] > 0):
            self._highlight = tuple([i * highlight_multiple for i in list(self._highlight)])
        else:
            self._highlight = list(self._highlight)
            val = max(self._highlight)
            
            for i, c in enumerate(self._highlight):
                if c == val:
                    self._highlight[i] *= highlight_multiple
            self._highlight = tuple(self._highlight)

        maxcol = 5.0

        self._color = (min(self._color[0], maxcol), min(self._color[1], maxcol), min(self._color[2], maxcol))

        self._highlight = (min(self._highlight[0], maxcol), min(self._highlight[1], maxcol), min(self._highlight[2], maxcol))

        self._update_icon()
        self._update_text()
    else:
        self.update_from_profile_glowing()

def _getname(self, full: bool = False) -> str:
    # Возвращает имя профиля, учитывая наличие "сияющего" эффекта.
    name_raw = name = self._profilenames[self._profileindex]
    if name[0] in self._glowing:
        name = name[1:]
        clamp = False
        if full:
            try:
                if self._profiles[name_raw].get('global', False):
                    icon = (self._profiles[name_raw]['icon']
                            if 'icon' in self._profiles[name_raw] else
                            _ba.charstr(SpecialChar.LOGO))
                    name = icon + name
            except Exception:
                print_exception('Error applying global icon.')
        else:
            clamp = True
        if clamp and len(name) > 10:
            name = name[:10] + '...'
        return name
    return self._getname_glowing(full)

def i_was_imported() -> bool:
    result = bool(getattr(ba.app, '_glowing_enabled', False))
    setattr(ba.app, '_glowing_enabled', True)
    return result

def redefine(methods: Dict[str, Callable]) -> None:
    for attr, obj in methods.items():
        if (hasattr(ba._lobby.Chooser, attr) and 
              not hasattr(ba._lobby.Chooser, attr + '_glowing')):
            setattr(ba._lobby.Chooser, attr + '_glowing',
                getattr(ba._lobby.Chooser, attr))
        setattr(ba._lobby.Chooser, attr, obj)

def main() -> None:
    if i_was_imported():
        return
    redefine({
        '__init__': __init__,
        'get_glowing': get_glowing,
        'update_from_profile': update_from_profile,
        '_getname': _getname
    })

main()

# ba_meta export plugin
class GlowingProfiles(ba.Plugin):
    def on_app_launch(self) -> None:
        pass
