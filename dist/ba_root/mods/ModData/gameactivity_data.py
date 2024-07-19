# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING

import time

import _ba, ba
from ba._gameactivity import GameActivity
from ba._teamgame import TeamGameActivity
from bastd.game.elimination import EliminationGame

def no_powerups(self):
    return

GameActivity.setup_standard_powerup_drops = no_powerups

old_on_begin = GameActivity.on_begin
def on_begin(self):
    old_on_begin(self)
    self.spawned_objects = []

    self.update_duelscoreboard()

    self.on_screen_text = {}
    try:
        self.show_server_name()
        self.show_server_restart_timer()
        self.show_server_credits()
        #self.show_server_rules()
        self.show_server_top()
    except:
        pass

    explosion = ba.newnode('explosion',
                           attrs={
                               'position': (0.0, 6.0, 0.0),
                               'velocity': (0.0, 0.0, 0.0),
                               'radius': 0.1,
                               'big': False,
                               'color': (0.0, 0.0, 0.0)
                           })

    on_screen_timer_interval = 15.0
    on_screen_show_interval = 13.0
    if self.globalsnode.slow_motion:
        on_screen_timer_interval /= 3.0
        on_screen_show_interval /= 3.0
    self.onScreenTextTimer = ba.Timer(on_screen_timer_interval, ba.Call(self.show_on_screen_text, on_screen_show_interval), repeat=True)

old_end = TeamGameActivity.end
def new_end(self,
            results: Any = None,
            announce_winning_team: bool = True,
            announce_delay: float = 0.1,
            force: bool = False) -> None:
    if not hasattr(self, 'blockend') or not self.blockend:
        old_end(self,
                results,
                announce_winning_team,
                announce_delay,
                force)


def update_duelscoreboard(self):
    from chatHandle.chat_functions import _light_green_, _clanwar_color_
    session = self.session
    if session.sessionmode == 'duelmode':
        from ModData.account_info import client_to_player
        score = self.session.duelscore
        duelplayers = self.session.duelplayers
        player_left_name = client_to_player(duelplayers[0].inputdevice.client_id)
        player_right_name = client_to_player(duelplayers[1].inputdevice.client_id)
        dueltext = player_left_name + '  ' + str(score[0]) + ':' + str(score[1]) + '  ' + player_right_name
        duelmaxtext = 'Дуэль до ' + str(self.session.duelscoretowin)
        self.duelscoreboard = ba.NodeActor(ba.newnode('text',
                                  attrs={
                                      'text': dueltext,
                                      'shadow': 1.0,
                                      'flatness': 1.0,
                                      'h_align': 'center',
                                      'v_attach': 'top',
                                      'scale': 1.0,
                                      'position': (5,-160),
                                      'color': _light_green_
                                  }))

        self.duelmaxtext = ba.NodeActor(ba.newnode('text',
                                  attrs={
                                      'text': duelmaxtext,
                                      'shadow': 1.0,
                                      'flatness': 1.0,
                                      'h_align': 'center',
                                      'v_attach': 'top',
                                      'scale': 1.0,
                                      'position': (5,-125),
                                      'color': _light_green_
                                  }))
    elif session.sessionmode == 'clanwar':
        score = self.session.clanwarscore
        team_left_name = self.session.clanwar_names[0]
        team_right_name = self.session.clanwar_names[1]
        clanwartext = team_left_name + '  ' + str(score[0]) + ':' + str(score[1]) + '  ' + team_right_name
        clanwarmaxtext = 'КВ до ' + str(self.session.clanwarscoretowin)
        self.duelscoreboard = ba.NodeActor(ba.newnode('text',
                                  attrs={
                                      'text': clanwartext,
                                      'shadow': 1.0,
                                      'flatness': 1.0,
                                      'h_align': 'center',
                                      'v_attach': 'top',
                                      'scale': 1.0,
                                      'position': (5,-160),
                                      'color': _clanwar_color_
                                  }))

        self.duelmaxtext = ba.NodeActor(ba.newnode('text',
                                  attrs={
                                      'text': clanwarmaxtext,
                                      'shadow': 1.0,
                                      'flatness': 1.0,
                                      'h_align': 'center',
                                      'v_attach': 'top',
                                      'scale': 1.0,
                                      'position': (5,-125),
                                      'color': _clanwar_color_
                                  }))

def delete_duelscoreboard(self):
    session = self.session
    if session.sessionmode not in ['dulemode', 'clanwar']:
        self.duelscoreboard = None
        self.duelmaxtext = None

def show_on_screen_text(self, time_interval):
    session = self.session
    server_data = session.serverData
    if 'text on map' in server_data:
        on_screen_text = []
        for playlist_name in server_data['text on map']:
            if playlist_name == 'all' or playlist_name == _ba.app.server._playlist_name:
                on_screen_text += server_data['text on map'][playlist_name]
        if len(on_screen_text) > 0:
            session.on_screen_text_index %= len(on_screen_text)
            self.set_on_screen_text(on_screen_text[session.on_screen_text_index], time_interval)
            session.on_screen_text_index = (session.on_screen_text_index + 1) % len(on_screen_text)

def set_on_screen_text(self, text, time_interval):
    self.on_screen_text['on_screen_message'] = _ba.newnode('text',
                                      attrs={
                                          'text': text,
                                          'shadow': 1.0,
                                          'flatness': 1.0,
                                          'h_align': 'center',
                                          'v_attach':'bottom',
                                          'scale': 1.0,
                                          'position':(0,5),
                                          'color':(1.0, 1.0, 1.0)
                                      })
    ba.animate(self.on_screen_text['on_screen_message'], 'opacity', {0.0: 0.0, 1.0: 1.0, time_interval - 1.0: 1.0, time_interval: 0.0})
    self.onScreenTextDeleteTimer = _ba.Timer(time_interval, self.delete_on_screen_text)

def delete_on_screen_text(self):
    self.on_screen_text['on_screen_message'].delete()


def show_server_name(self):
    self.on_screen_text['servername'] = _ba.newnode('text',
                                      attrs={
                                          'text': _ba.app.server._config.party_name,
                                          'shadow': 1.0,
                                          'flatness': 1.0,
                                          'h_align': 'center',
                                          'v_attach':'top',
                                          'scale':1.3,
                                          'position':(5,-50),
                                          'color':(1.0, 1.0, 1.0)
                                      })

def show_server_restart_timer(self):
    self.on_screen_text['serverrestarttimer'] = _ba.newnode('text',
                                      attrs={
                                          'text': 'restart in:',
                                          'shadow': 1.0,
                                          'flatness': 1.0,
                                          'h_align': 'center',
                                          'v_attach':'top',
                                          'scale':0.6,
                                          'position':(-35,-70),
                                          'color':(0.4, 0.35, 0.25),
                                          'opacity': 0.85
                                      })
    self.on_screen_text['servertime'] = _ba.newnode('text',
                                      attrs={
                                          'text': '',
                                          'shadow': 1.0,
                                          'flatness': 1.0,
                                          'h_align': 'left',
                                          'v_attach':'top',
                                          'scale':0.6,
                                          'position':(5,-70.5),
                                          'color':(0.0, 1.0, 0.0),
                                          'opacity': 0.75
                                      })
    self.serverTimer = _ba.Timer(0.05, self._update_server_time, repeat=True)

def _update_server_time(self):
    cur_time = int(_ba.app.server._config.unclean_exit_minutes * 60.0 - (time.time() - self.session.starttime))
    cur_hours = int(cur_time / 60.0 / 60.0)
    cur_min = int(cur_time / 60.0) % 60
    cur_sec = cur_time % 60
    if cur_time < 0.3:
        self.on_screen_text['servertime'].color = (1.0, 0.0, 0.0)
        self.on_screen_text['servertime'].text = 'RESTARTING...'
    else:
        if cur_min < 10:
            self.on_screen_text['servertime'].color = (1.0, 0.0, 0.3)
        elif cur_min < 30:
            self.on_screen_text['servertime'].color = (1.0, 1.0, 0.3)
        else:
            self.on_screen_text['servertime'].color = (0.1, 1.0, 0.3)
        self.on_screen_text['servertime'].text = ''
        if cur_hours > 0:
            self.on_screen_text['servertime'].text += str(cur_hours) + 'h '
        self.on_screen_text['servertime'].text += str(cur_min) + 'm ' + str(cur_sec) + 's'

def show_server_credits(self):
    text = ''
    session = self.session
    server_data = session.serverData
    if 'credits' in server_data:
        for line in server_data['credits']:
            if text != '':
                text += '\n'
            text += line
    self.on_screen_text['credits'] = _ba.newnode('text',
                                      attrs={
                                          'text': text,
                                          'shadow': 1.0,
                                          'flatness': 1.0,
                                          'h_align': 'left',
                                          'v_align': 'bottom',
                                          'h_attach': 'left',
                                          'v_attach': 'bottom',
                                          'scale': 0.7,
                                          'position': (10,80),
                                          'color': (0.9, 0.9, 0.9),
                                          'opacity': 0.8
                                      })
    self.on_screen_text['credits2'] = _ba.newnode('text',
                                      attrs={
                                          'text': 'NewMod v 1.0 by gtex',
                                          'shadow': 0.0,
                                          'flatness': 0.0,
                                          'h_align': 'right',
                                          'v_align': 'bottom',
                                          'h_attach': 'right',
                                          'v_attach': 'bottom',
                                          'scale': 0.85,
                                          'position': (-20, 3),
                                          'color': (0.7, 0.7, 0.7),
                                          'opacity': 0.4
                                      })

def show_server_rules(self):
    text = ''
    session = self.session
    server_data = session.serverData
    if 'rules' in server_data:
        for line in server_data['rules']:
            if text != '':
                text += '\n'
            text += line
    self.on_screen_text['rules'] = _ba.newnode('text',
                                      attrs={
                                          'text': text,
                                          'shadow': 1.0,
                                          'flatness': 1.0,
                                          'h_align': 'left',
                                          'v_align': 'top',
                                          'h_attach': 'left',
                                          'v_attach': 'top',
                                          'scale': 0.7,
                                          'position': (10,-200),
                                          'color': (0.9, 0.9, 0.9)
                                      })

def show_server_top(self):
    session = self.session
    server_data = session.serverData
    if 'season' in server_data:
        season_num = server_data['season']
    else:
        season_num = 1
    self.on_screen_text['season_name'] = _ba.newnode('text',
                                      attrs={
                                          'text': 'Сезон: ' + (str(season_num) if 'top reset date' in server_data else ''),
                                          'shadow': 1.0,
                                          'flatness': 1.0,
                                          'h_align': 'left',
                                          'v_align': 'top',
                                          'h_attach': 'right',
                                          'v_attach': 'top',
                                          'scale': 0.5,
                                          'position': (-115,-56),
                                          'color': (0.5, 1.0, 0.5),
                                          'opacity': 0.75
                                      })
    if 'top reset date' in server_data:
        time_interval = time.mktime(time.strptime(server_data['top reset date'])) - time.time()
        if time_interval < 0.0:
            days = 0
            hours = 0
        else:
            days = int(time_interval / 24.0 / 60.0 / 60.0)
            hours = int(time_interval / 60.0 / 60.0) - days * 24
        if days == 0 and hours == 0:
            text = 'ожидает ресета'
        else:
            text = 'Сброс через: ' + str(days) + 'd ' + str(hours) + 'h'
    else:
        text = 'начните новый сезон!'
    self.on_screen_text['update_info'] = _ba.newnode('text',
                                  attrs={
                                      'text': text,
                                      'shadow': 1.0,
                                      'flatness': 1.0,
                                      'h_align': 'left',
                                      'v_align': 'top',
                                      'h_attach':'right',
                                      'v_attach':'top',
                                      'scale':0.65,
                                      'position':(-180,-73),
                                      'color': (0.8, 0.8, 0.8),
                                      'opacity': 0.75
                                  })
    from ModData.ranking import get_rank, get_top_list
    session = self.session
    toplist = session.playersData['toplist']
    if len(toplist) > 10:
        toplist = toplist[:10]
    toptext = ''
    for account_id in toplist:
        if toptext != '': toptext += '\n'
        player_name = account_id
        if len(session.playersData['stats'][account_id]['account name']) != 0:
            player_name = session.playersData['stats'][account_id]['account name'][-1]
        if session.playersData['stats'][account_id]['last player name'] != '':
            player_name = session.playersData['stats'][account_id]['last player name']
        toptext += '#' + str(get_rank(account_id)) + ' ' + player_name
    #if _ba.app.server._playlist_name == 'фортон 99':
    if True:
        self.on_screen_text['toplist'] = _ba.newnode('text',
                                          attrs={
                                              'text': toptext,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'h_align': 'left',
                                              'v_align': 'top',
                                              'h_attach': 'right',
                                              'v_attach': 'top',
                                              'scale': 0.65,
                                              'position': (-185,-92),
                                              'color': (0.8, 0.8, 0.8),
                                              'opacity': 0.75
                                          })
    session = self.session
    server_data = session.serverData
    if 'topcolor' in server_data:
        topcolor = server_data['topcolor']
        self.change_node_color(self.on_screen_text['season_name'], 'color', topcolor)
        if self.on_screen_text['update_info'] != None:
            self.change_node_color(self.on_screen_text['update_info'], 'color', topcolor)
        self.change_node_color(self.on_screen_text['toplist'], 'color', topcolor)


from ba._messages import PlayerDiedMessage

old_handlemessage = GameActivity.handlemessage
def new_handlemessage(self, msg: Any) -> Any:
    if isinstance(msg, PlayerDiedMessage):
        # pylint: disable=cyclic-import
        from bastd.actor.spaz import Spaz

        player = msg.getplayer(self.playertype)
        killer = msg.getkillerplayer(self.playertype)

        try:
            session = self.session
            if session.sessionmode == 'duelmode':
                if player.sessionplayer == session.duelplayers[0]:
                    session.duelscore[1] += 1
                    self.update_duelscoreboard()
                    if session.duelscore[1] >= session.duelscoretowin:
                        session.end_duel()
                    if killer.actor and not killer.actor._dead and session.duelheal:
                        killer.actor.hitpoints = killer.actor.hitpoints_max
                        killer.actor.node.hurt = 0
                elif player.sessionplayer == session.duelplayers[1]:
                    session.duelscore[0] += 1
                    self.update_duelscoreboard()
                    if session.duelscore[0] >= session.duelscoretowin:
                        session.end_duel()
                    if killer.actor and not killer.actor._dead and session.duelheal:
                        killer.actor.hitpoints = killer.actor.hitpoints_max
                        killer.actor.node.hurt = 0
        except:
            pass

        # Inform our stats of the demise.
        self.stats.player_was_killed(player,
                                     killed=msg.killed,
                                     killer=killer)

        # Award the killer points if he's on a different team.
        # FIXME: This should not be linked to Spaz actors.
        # (should move get_death_points to Actor or make it a message)
        if killer and killer.team is not player.team:
            assert isinstance(killer.actor, Spaz)
            pts, importance = killer.actor.get_death_points(msg.how)
            if not self.has_ended():
                self.stats.player_scored(killer,
                                         pts,
                                         kill=True,
                                         victim_player=player,
                                         importance=importance,
                                         showpoints=self.show_kill_points)
    else:
        return old_handlemessage(self, msg)
    return None

old_elimination_handlemessage = EliminationGame.handlemessage
def elimination_handlemessage(self, msg: Any) -> Any:
    res = old_elimination_handlemessage(self, msg)
    if isinstance(msg, PlayerDiedMessage):
        if self.session.sessionmode == 'clanwar' and (not hasattr(self, 'clanwar_round_ended') or not self.clanwar_round_ended):
            team_lost = True
            for player in self.session.clanwar_teams[0]:
                if player.activityplayer and player.activityplayer.lives > 0:
                    team_lost = False
            if team_lost:
                self.session.clanwarscore[1] += 1
                self.update_duelscoreboard()
                self.clanwar_round_ended = True
                if self.session.clanwarscore[1] >= self.session.clanwarscoretowin:
                    self.session.end_clanwar()
                self.end_game()
            else:
                team_lost = True
                for player in self.session.clanwar_teams[1]:
                    if player.activityplayer and player.activityplayer.lives > 0:
                        team_lost = False
                if team_lost:
                    self.session.clanwarscore[0] += 1
                    self.update_duelscoreboard()
                    self.clanwar_round_ended = True
                    if self.session.clanwarscore[0] >= self.session.clanwarscoretowin:
                        self.session.end_clanwar()
                    self.end_game()
    return res

TeamGameActivity.end = new_end
GameActivity.on_begin = on_begin
GameActivity.update_duelscoreboard = update_duelscoreboard
GameActivity.delete_duelscoreboard = delete_duelscoreboard
GameActivity.show_on_screen_text = show_on_screen_text
GameActivity.set_on_screen_text = set_on_screen_text
GameActivity.delete_on_screen_text = delete_on_screen_text
GameActivity.show_server_name = show_server_name
GameActivity.show_server_restart_timer = show_server_restart_timer
GameActivity._update_server_time = _update_server_time
GameActivity.show_server_credits = show_server_credits
GameActivity.show_server_rules = show_server_rules
GameActivity.show_server_top = show_server_top
GameActivity.handlemessage = new_handlemessage
EliminationGame.handlemessage = elimination_handlemessage
