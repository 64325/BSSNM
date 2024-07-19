# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING

import time

import _ba, ba
from bastd.actor import playerspaz
from ba import _player
from ModData.strings import *


old__init__ = playerspaz.PlayerSpaz.__init__
def new__init__(self,
                player: ba.Player,
                color: Sequence[float] = (1.0, 1.0, 1.0),
                highlight: Sequence[float] = (0.5, 0.5, 0.5),
                character: str = 'Spaz',
                powerups_expire: bool = True):
    old__init__(self,
                player,
                color,
                highlight,
                character,
                powerups_expire)
    self._add_effects()
    _customize(self)

def _customize(self):
    character = self.getplayer(ba.Player).character
    if character not in _ba.app.spaz_appearances:
        return
    appearance = _ba.app.spaz_appearances[character]
    if hasattr(appearance, 'custom_effects'):
        appearance.custom_effects(self)

def _add_effects(self):
    self.set_tag()
    self.set_ranktag()
    self.set_rgb()
    self.set_punchcolor()
    self.particle_spawner = None
    self.set_particles()

def set_tag(self):
    if not self.node:
        return
    activity = ba.getactivity()
    session = activity.session
    from ModData.account_info import client_to_account
    account_id = client_to_account(self._player.sessionplayer.inputdevice.client_id)
    if account_id in session.playersData['effects'] and 'tag' in session.playersData['effects'][account_id]:
        from actors.tag import Tag
        text = session.playersData['effects'][account_id]['tag']['text']
        if 'size' in session.playersData['effects'][account_id]['tag']:
            size = session.playersData['effects'][account_id]['tag']['size']
        else:
            size = 1.0
        self.tag = Tag(self,
                       text=text,
                       size=size)
        if 'color' in session.playersData['effects'][account_id]['tag']:
            activity.change_node_color(self.tag.node, 'color', session.playersData['effects'][account_id]['tag']['color'])
        elif 'animation' in session.playersData['effects'][account_id]['tag']:
            activity.start_node_animation(self.tag.node, 'color', session.playersData['effects'][account_id]['tag']['animation'])
    self.set_ranktag()

def remove_tag(self):
    self.tag = None
    self.set_ranktag()

def set_ranktag(self):
    if not self.node:
        return
    self.remove_ranktag()
    activity = ba.getactivity()
    session = activity.session
    from ModData.account_info import client_to_account
    account_id = client_to_account(self._player.sessionplayer.inputdevice.client_id)
    if account_id in session.playersData['effects'] and 'stat' in session.playersData['effects'][account_id] and session.playersData['effects'][account_id]['stat']:
        return
    from ModData.ranking import get_rank
    rank = get_rank(account_id)
    from actors.tag import RankTag
    self.ranktag = RankTag(self,
                       rank=rank)
    if account_id in session.playersData['effects'] and 'statcolor' in session.playersData['effects'][account_id]:
        if 'color' in session.playersData['effects'][account_id]['statcolor']:
            activity.change_node_color(self.ranktag.node, 'color', session.playersData['effects'][account_id]['statcolor']['color'])
        elif 'animation' in session.playersData['effects'][account_id]['statcolor']:
            activity.start_node_animation(self.ranktag.node, 'color', session.playersData['effects'][account_id]['statcolor']['animation'])
    elif hasattr(self, 'tag') and self.tag != None:
        self.tag.node.connectattr('color', self.ranktag.node, 'color')

def remove_ranktag(self):
    self.ranktag = None

def set_rgb(self):
    activity = ba.getactivity()
    session = activity.session
    from ModData.account_info import client_to_account
    account_id = client_to_account(self._player.sessionplayer.inputdevice.client_id)
    if account_id in session.playersData['effects'] and 'rgb' in session.playersData['effects'][account_id]:
        from actors.rgb_glow import RGBGlow
        if 'size' in session.playersData['effects'][account_id]['rgb']:
            size = session.playersData['effects'][account_id]['rgb']['size']
        else:
            size = 1.0
        self.rgb = RGBGlow(self,
                       size=size)
        if 'color' in session.playersData['effects'][account_id]['rgb']:
            activity.change_node_color(self.rgb.node, 'color', session.playersData['effects'][account_id]['rgb']['color'])
        elif 'animation' in session.playersData['effects'][account_id]['rgb']:
            activity.start_node_animation(self.rgb.node, 'color', session.playersData['effects'][account_id]['rgb']['animation'])

def remove_rgb(self):
    self.rgb = None

def set_punchcolor(self):
    activity = ba.getactivity()
    session = activity.session
    from ModData.account_info import client_to_account
    account_id = client_to_account(self._player.sessionplayer.inputdevice.client_id)
    if account_id in session.playersData['effects'] and 'punchcolor' in session.playersData['effects'][account_id]:
        self.punchcolor = session.playersData['effects'][account_id]['punchcolor']['color']
    else:
        self.punchcolor = []

def remove_ranktag(self):
    self.ranktag = None

def set_particles(self):
    self.remove_particles()
    activity = ba.getactivity()
    session = activity.session
    from ModData.account_info import client_to_account
    account_id = client_to_account(self._player.sessionplayer.inputdevice.client_id)
    if account_id in session.playersData['effects'] and 'particles' in session.playersData['effects'][account_id]:
        from actors.particle import ParticleSpawner
        type = session.playersData['effects'][account_id]['particles']['type']
        size = session.playersData['effects'][account_id]['particles']['size']
        if 'time_interval' in session.playersData['effects'][account_id]['particles']:
            time_interval = session.playersData['effects'][account_id]['particles']['time_interval']
        else:
            time_interval = session.playersData['effects'][account_id]['particles']['time interval']
        self.particle_spawner = ParticleSpawner(self,
                       type=type,
                       size=size,
                       time_interval=time_interval)

def remove_particles(self):
    if self.particle_spawner != None:
        self.particle_spawner.handlemessage(ba.DieMessage())
        self.particle_spawner = None


playerspaz.PlayerSpaz._add_effects = _add_effects
playerspaz.PlayerSpaz.set_tag = set_tag
playerspaz.PlayerSpaz.remove_tag = remove_tag
playerspaz.PlayerSpaz.set_ranktag = set_ranktag
playerspaz.PlayerSpaz.remove_ranktag = remove_ranktag
playerspaz.PlayerSpaz.set_rgb = set_rgb
playerspaz.PlayerSpaz.remove_rgb = remove_rgb
playerspaz.PlayerSpaz.set_punchcolor = set_punchcolor
playerspaz.PlayerSpaz.set_particles = set_particles
playerspaz.PlayerSpaz.remove_particles = remove_particles
playerspaz.PlayerSpaz.__init__ = new__init__


old_postinit = _player.Player.postinit
def new_postinit(self, sessionplayer: ba.SessionPlayer) -> None:
    old_postinit(self, sessionplayer)
    from ModData.account_info import client_to_account
    account_id = client_to_account(sessionplayer.inputdevice.client_id)
    session = _ba.get_foreground_host_session()
    if account_id in session.playersData['effects'] and 'skin' in session.playersData['effects'][account_id]:
        self.character = session.playersData['effects'][account_id]['skin']
    if account_id in session.localPlayersData['effects'] and 'skin' in session.localPlayersData['effects'][account_id]:
        self.character = session.localPlayersData['effects'][account_id]['skin']

_player.Player.postinit = new_postinit
