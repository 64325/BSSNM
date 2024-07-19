# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING

import time
import os
import random

import _ba
from ba._session import Session
from ba._coopsession import CoopSession
from ba._servermode import ServerController
from ModData.strings import *

old__init__ = Session.__init__
def new__init__(self,
                depsets: Sequence[ba.DependencySet],
                team_names: Sequence[str] | None = None,
                team_colors: Sequence[Sequence[float]] | None = None,
                min_players: int = 1,
                max_players: int = 8):
    old__init__(self,
                depsets,
                team_names,
                team_colors,
                min_players,
                max_players)
    self._postinit()

def _postinit(self):
    self.max_players = 25
    self.lobby_blocked = False
    self.sessionmode = 'normal'
    self.starttime = time.time()
    self.load_session_data()

def load_session_data(self):
    self.playersData = {}
    self.localPlayersData = {}
    self.localPlayersData['effects'] = {}
    self.localPlayersData['chat_entries'] = {}
    self.localPlayersData['mutelist'] = {}
    self.load_stats()
    self.statsTimer = _ba.Timer(180.0, self.update_stats, repeat=True)
    self.update_banlist()
    self.updateBanlistTimer = _ba.Timer(60.0, self.update_banlist, repeat=True)
    self.localPlayersData['accepted_clients'] = []
    self.kickTimer = _ba.Timer(1.0, self.kick_banned_players, repeat=True)
    self.update_mutelist()
    self.updateMutelistTimer = _ba.Timer(10.0, self.update_mutelist, repeat=True)
    self.update_warnlist()
    self.updateWarnlistTimer = _ba.Timer(60.0, self.update_warnlist, repeat=True)
    self.update_effects()
    self.updateEffectsTimer = _ba.Timer(60.0, self.update_effects, repeat=True)
    self.update_allow_data()
    self.updateAllowDataTimer = _ba.Timer(60.0, self.update_allow_data, repeat=True)
    self.update_roles()
    self.updateRolesTimer = _ba.Timer(60.0, self.update_roles, repeat=True)
    self.serverData = {}
    self.load_server_data()
    self.serverDataTimer = _ba.Timer(180.0, self.load_server_data, repeat=True)
    self.update_waiting_messages()
    self.updateWaitingMessagesTimer = _ba.Timer(8.0, self.update_waiting_messages, repeat=True)
    self.on_screen_text_index = 0
    #self.onScreenTextTimer = _ba.Timer(240.0, self.show_on_screen_text, repeat=True)
    self.playersData['cooldown'] = {}
    

def load_stats(self):
    from ModData import stats
    try:
        self.playersData['stats'] = stats.load_stats()
        stats.backup_stats()
    except:
        if not 'stats' in self.playersData:
            self.playersData['stats'] = {}
    self.localPlayersData['stats'] = {}
    for player in self.sessionplayers:
        self.add_player_to_local_stats(player)
    from ModData.ranking import get_top_list
    self.playersData['toplist'] = get_top_list()

def add_player_to_local_stats(self, player):
    from ModData import stats
    from ModData import account_info
    account_id = account_info.client_to_account(player.inputdevice.client_id)
    account_name = account_info.client_to_display_string(player.inputdevice.client_id)
    if account_id != '' and account_id not in self.localPlayersData['stats']:
        self.localPlayersData['stats'][account_id] = stats.create_profile(account_name)

def update_stats(self):
    from ModData import stats
    try:
        stats.update_stats(self.localPlayersData['stats'])
        stats.load_stats()
        self.update_stats_fails = 0
    except:
        if not hasattr(self, 'update_stats_fails'):
            self.update_stats_fails = 0
        self.update_stats_fails += 1
        if self.update_stats_fails < 4:
            stats.recover_stats()
            _ba.timer(random.uniform(8.0, 12.0), self.update_stats)
            return
        else:
            _ba.chatmessage(stats_not_available_str)
            if not hasattr(self, 'stats_not_available_msg_sent'):
                self.stats_not_available_msg_sent = True
                print(stats_not_available_str)
    self.load_stats()

def update_banlist(self):
    from ModData import ban
    try:
        self.playersData['banlist'] = ban.load_banlist()
        ban.save_banlist(self.playersData['banlist'])
    except:
        self.playersData['banlist'] = {}
        if not hasattr(self, 'banlist_not_available_msg_sent'):
            self.banlist_not_available_msg_sent = True
            print(banlist_not_available_str)

def kick_banned_players(self):
    self.localPlayersData['accepted_clients'] = []
    from ModData import account_info
    _red_ = (1.0, 0.1, 0.0)
    rost = _ba.get_game_roster()
    for i in rost:
        account_id = account_info.client_to_account(i['client_id'])
        account_name = account_info.client_to_display_string(i['client_id'])
        if account_id in self.playersData['banlist']:
            _ba.screenmessage(banned_str, color = _red_, transient=True, clients=[i['client_id']])
            if 'reason' in self.playersData['banlist'][account_id]:
                _ba.screenmessage(self.playersData['banlist'][account_id]['reason'], color = _red_, transient=True, clients=[i['client_id']])
            if 'until' in self.playersData['banlist'][account_id] and time.mktime(time.strptime(self.playersData['banlist'][account_id]['until'])) < time.time() + 300.0:
                _ba.disconnect_client(i['client_id'], ban_time=int(time.mktime(time.strptime(self.playersData['banlist'][account_id]['until'])) - time.time() + 1))
            else:
                _ba.disconnect_client(i['client_id'])
        elif account_name != '' and account_name in self.playersData['banlist']:
            _ba.screenmessage(banned_str, color = _red_, transient=True, clients=[i['client_id']])
            if 'reason' in self.playersData['banlist'][account_name]:
                _ba.screenmessage(self.playersData['banlist'][account_name]['reason'], color = _red_, transient=True, clients=[i['client_id']])
            if 'until' in self.playersData['banlist'][account_name] and time.mktime(time.strptime(self.playersData['banlist'][account_name]['until'])) < time.time() + 300.0:
                _ba.disconnect_client(i['client_id'], ban_time=int(time.mktime(time.strptime(self.playersData['banlist'][account_name]['until'])) - time.time() + 1))
            else:
                _ba.disconnect_client(i['client_id'])
        else:
            self.localPlayersData['accepted_clients'].append(i['client_id'])

def update_mutelist(self):
    from ModData import mute
    try:
        self.playersData['mutelist'] = mute.load_mutelist()
        mute.save_mutelist(self.playersData['mutelist'])
    except:
        self.playersData['mutelist'] = {}
        if not hasattr(self, 'mutelist_not_available_msg_sent'):
            self.mutelist_not_available_msg_sent = True
            print(mutelist_not_available_str)

def update_warnlist(self):
    from ModData import warn
    try:
        self.playersData['warnlist'] = warn.load_warnlist()
        warn.save_warnlist(self.playersData['warnlist'])
    except:
        self.playersData['warnlist'] = {}
        if not hasattr(self, 'warnlist_not_available_msg_sent'):
            self.warnlist_not_available_msg_sent = True
            print(warnlist_not_available_str)

def update_effects(self):
    from ModData import effects
    try:
        self.playersData['effects'] = effects.load_effects()
    except:
        self.playersData['effects'] = {}
        if not hasattr(self, 'effects_not_available_msg_sent'):
            self.effects_not_available_msg_sent = True
            print(effects_not_available_str)

def update_allow_data(self):
    from ModData import allow
    try:
        self.playersData['allow_data'] = allow.load_allow_data()
        allow.save_allow_data(self.playersData['allow_data'])
    except:
        self.playersData['allow_data'] = []
        if not hasattr(self, 'allow_data_not_available_msg_sent'):
            self.allow_data_not_available_msg_sent = True
            print(allow_data_not_available_str)

def update_roles(self):
    from ModData import roles
    try:
        self.playersData['roles'] = roles.load_roles()
        roles.save_roles(self.playersData['roles'])
    except:
        self.playersData['roles'] = {}
        if not hasattr(self, 'roles_not_available_msg_sent'):
            self.roles_not_available_msg_sent = True
            print(roles_not_available_str)

def load_server_data(self):
    from ModData import server_data
    try:
        self.serverData = server_data.load_server_data()
    except:
        self.serverData = {}
        _ba.chatmessage(server_data_not_available_str)
        if not hasattr(self, 'server_data_not_available_msg_sent'):
            self.server_data_not_available_msg_sent = True
            print(server_data_not_available_str)
    from ModData import server_roles
    try:
        self.serverData['server_roles'] = server_roles.load_server_roles()
        from chatCommands.Commands import Creator, Admins, Players
        for role in self.serverData['server_roles']:
            old_commands_list = self.serverData['server_roles'][role]['commands']
            new_commands_list = []
            from ModData.me import get_value
            if role == 'CREATOR':
                packages = [Creator, Admins, Players]
            elif get_value(role) > 0:
                packages = [Admins, Players]
            else:
                packages = [Players]
            for package in packages:
                for command_name in package.__all__:
                    if ('all' in old_commands_list or command_name in old_commands_list) and '-' + command_name not in old_commands_list:
                        if command_name not in new_commands_list:
                            new_commands_list.append(command_name)
            self.serverData['server_roles'][role]['commands'] = new_commands_list
    except:
        self.serverData['server_roles'] = {}
        _ba.chatmessage(server_roles_not_available_str)
        if not hasattr(self, 'server_roles_not_available_msg_sent'):
            self.server_roles_not_available_msg_sent = True
            print(server_roles_not_available_str)

def update_waiting_messages(self):
    try:
        from ModData import waiting_message
        waiting_messages = waiting_message.load_messages()
        rost = _ba.get_game_roster()
        for i in rost:
            acc_id = i['account_id']
            cl_id = i['client_id']
            if acc_id in waiting_messages:
                _ba.screenmessage(waiting_messages[acc_id]['messages'][0], color=waiting_messages[acc_id]['colors'][0], transient=True, clients=[cl_id])
                waiting_message.pop_message(acc_id)
    except:
        pass

def show_on_screen_text(self):
    server_data = self.serverData
    if 'text on map' in server_data:
        on_screen_text = []
        for playlist_name in server_data['text on map']:
            if playlist_name == 'all' or playlist_name == _ba.app.server._playlist_name:
                on_screen_text += server_data['text on map'][playlist_name]
        if len(on_screen_text) > 0:
            self.on_screen_text_index %= len(on_screen_text)
            _ba.screenmessage(on_screen_text[self.on_screen_text_index], color=(1.0, 1.0, 1.0), transient=True)
            self.on_screen_text_index = (self.on_screen_text_index + 1) % len(on_screen_text)


def start_duel(self, sessionplayer_left, sessionplayer_right, scoretowin, heal=False):
    if self.sessionmode == 'clanwar':
        self.end_clanwar()
    from ModData.account_info import client_to_player
    from chatHandle.chat_functions import showmessage, _light_green_
    self.duelplayers = [sessionplayer_left, sessionplayer_right]
    self.duelscore = [0, 0]
    self.duelscoretowin = scoretowin
    self.duelheal = heal
    for player in list(self.sessionplayers):
        if player != sessionplayer_left and player != sessionplayer_right:
            player.remove_from_game()
    player_left_name = client_to_player(self.duelplayers[0].inputdevice.client_id)
    player_right_name = client_to_player(self.duelplayers[1].inputdevice.client_id)
    self.sessionmode = 'duelmode'
    try:
        activity = self._activity_weak()
        activity.update_duelscoreboard()
    except:
        pass
    showmessage(-1, 2, 'начата дуэль ' + player_left_name + ' vs ' + player_right_name + ' до ' + str(self.duelscoretowin) + ' очков', _light_green_)

def set_duelscoretowin(self, scoretowin):
    self.duelscoretowin = scoretowin
    self.update_duel()

def update_duel(self):
    try:
        activity = self._activity_weak()
        activity.update_duelscoreboard()
    except:
        pass

def end_duel(self):
    if self.sessionmode != 'duelmode':
        return
    from ModData.account_info import client_to_player
    from chatHandle.chat_functions import showmessage, _light_green_
    player_left_name = client_to_player(self.duelplayers[0].inputdevice.client_id)
    player_right_name = client_to_player(self.duelplayers[1].inputdevice.client_id)
    activity = _ba.get_foreground_host_activity()
    try:
        activity = self._activity_weak()
        _ba.timer(0.7, activity.delete_duelscoreboard)
    except:
        pass
    self.sessionmode = 'usual'
    if self.duelscore[0] >= self.duelscoretowin or self.duelscore[1] >= self.duelscoretowin:
        if self.duelscore[0] == self.duelscore[1]:
            showmessage(-1, 2, 'дуэль завершилась вничью со счётом ' + str(self.duelscore[0]) + ':' + str(self.duelscore[1]), _light_green_)
            return
        elif self.duelscore[0] > self.duelscore[1]:
            showmessage(-1, 2, 'дуэль завершилась со счётом ' + str(self.duelscore[0]) + ':' + str(self.duelscore[1]) + ', победил ' + player_left_name, _light_green_)
            return
        else:
            showmessage(-1, 2, 'дуэль завершилась со счётом ' + str(self.duelscore[0]) + ':' + str(self.duelscore[1]) + ', победил ' + player_right_name, _light_green_)
            return
    showmessage(-1, 2, 'дуэль завершилась со счётом ' + str(self.duelscore[0]) + ':' + str(self.duelscore[1]), _light_green_)

def start_clanwar(self, accounts_left, accounts_right, team_left, team_right, scoretowin):
    if self.sessionmode == 'duelmode':
        self.end_duel()
    from chatHandle.chat_functions import showmessage, _clanwar_color_
    self.clanwar_accounts = [accounts_left, accounts_right]
    self.clanwar_teams = [team_left, team_right]
    self.clanwarscore = [0, 0]
    self.clanwarscoretowin = scoretowin
    for player in list(self.sessionplayers):
        if player not in team_left and player not in team_right:
            player.remove_from_game()
    self.clanwar_names = ['Team1', 'Team2']
    self.sessionmode = 'clanwar'
    try:
        activity = self._activity_weak()
        #activity.update_duelscoreboard()
        activity.clanwar_round_ended = True
        activity.blockend = False
        activity.end_game()
    except:
        pass
    showmessage(-1, 2, 'начата клановая война ' + ' до ' + str(self.clanwarscoretowin) + ' очков', _clanwar_color_)

def set_clanwar_name_left(self, name):
    self.clanwar_names[0] = name
    self.update_clanwar()

def set_clanwar_name_right(self, name):
    self.clanwar_names[1] = name
    self.update_clanwar()

def set_clanwarscoretowin(self, score):
    self.clanwarscoretowin = score
    self.update_clanwar()

def update_clanwar(self):
    try:
        activity = self._activity_weak()
        activity.update_duelscoreboard()
    except:
        pass

def end_clanwar(self):
    if self.sessionmode != 'clanwar':
        return
    from ModData.account_info import client_to_player
    from chatHandle.chat_functions import showmessage, _clanwar_color_
    try:
        activity = self._activity_weak()
        _ba.timer(0.7, activity.delete_duelscoreboard)
    except:
        pass
    self.sessionmode = 'usual'
    if self.clanwarscore[0] >= self.clanwarscoretowin or self.clanwarscore[1] >= self.clanwarscoretowin:
        if self.clanwarscore[0] == self.clanwarscore[1]:
            showmessage(-1, 2, 'кв завершилась вничью со счётом ' + str(self.clanwarscore[0]) + ':' + str(self.clanwarscore[1]), _clanwar_color_)
            return
        elif self.clanwarscore[0] > self.clanwarscore[1]:
            showmessage(-1, 2, 'кв завершилась со счётом ' + str(self.clanwarscore[0]) + ':' + str(self.clanwarscore[1]) + ', победили ' + self.clanwar_names[0], _clanwar_color_)
            return
        else:
            showmessage(-1, 2, 'кв завершилась со счётом ' + str(self.clanwarscore[0]) + ':' + str(self.clanwarscore[1]) + ', победили ' + self.clanwar_names[1], _clanwar_color_)
            return
    showmessage(-1, 2, 'кв завершилась со счётом ' + str(self.clanwarscore[0]) + ':' + str(self.clanwarscore[1]), _clanwar_color_)


old_on_player_request = Session.on_player_request
def on_player_request(self, player: ba.SessionPlayer) -> bool:
    if old_on_player_request(self, player):
        self.add_player_to_local_stats(player)
        return True
    else:
        return False

def _request_player(self, sessionplayer: ba.SessionPlayer) -> bool:
    """Called by the native layer when a player wants to join."""

    # If we're ending, allow no new players.
    if self._ending:
        return False

    _light_yellow_ = (1.0, 0.85, 0.3)

    cl_id = sessionplayer.inputdevice.client_id
    for player in self.sessionplayers:
        if cl_id == player.inputdevice.client_id:
            _ba.screenmessage(only_1_account_str, transient=True, clients=[cl_id], color=_light_yellow_)
            return False
        from ModData.account_info import client_to_display_string
        account_name = client_to_display_string(cl_id)
        if account_name == client_to_display_string(player.inputdevice.client_id):
            _ba.screenmessage(account_already_joined_str, transient=True, clients=[cl_id], color=_light_yellow_)
            return False

    if not hasattr(self, 'lobby_blocked'):
        print('no')
    elif not hasattr(self, 'lobby_blocked') or self.lobby_blocked:
        cl_id = sessionplayer.inputdevice.client_id
        _ba.screenmessage(lobby_blocked_str, transient=True, clients=[cl_id], color=_light_yellow_)
        return False
    elif self.sessionmode == 'duelmode':
        cl_id = sessionplayer.inputdevice.client_id
        _ba.screenmessage(duel_running_str, transient=True, clients=[cl_id], color=_light_yellow_)
        return False
    elif self.sessionmode == 'clanwar':
        cl_id = sessionplayer.inputdevice.client_id
        from ModData.account_info import client_to_display_string
        account_name = client_to_display_string(cl_id)
        if not (account_name in self.clanwar_accounts[0] or account_name in self.clanwar_accounts[1]):
            _ba.screenmessage(clanwar_running_str, transient=True, clients=[cl_id], color=_light_yellow_)
            return False

    # Ask the ba.Session subclass to approve/deny this request.
    try:
        with _ba.Context(self):
            result = self.on_player_request(sessionplayer)
    except Exception:
        print_exception(f'Error in on_player_request for {self}')
        result = False

    # If they said yes, add the player to the lobby.
    if result:
        self.sessionplayers.append(sessionplayer)
        if self.sessionmode == 'clanwar':
            cl_id = sessionplayer.inputdevice.client_id
            from ModData.account_info import client_to_display_string
            account_name = client_to_display_string(cl_id)
            if account_name in self.clanwar_accounts[0]:
                self.clanwar_teams[0].append(sessionplayer)
            elif account_name in self.clanwar_accounts[1]:
                self.clanwar_teams[1].append(sessionplayer)

        with _ba.Context(self):
            try:
                self.lobby.add_chooser(sessionplayer)
            except Exception:
                print_exception('Error in lobby.add_chooser().')

    return result

old_on_player_ready = Session._on_player_ready
def _on_player_ready(self, chooser: ba.Chooser) -> None:
    old_on_player_ready(self, chooser)

    from ModData.account_info import client_to_account
    account_id = client_to_account(chooser.getplayer().inputdevice.client_id)
    if account_id in self.localPlayersData['stats']:
        self.localPlayersData['stats'][account_id]['last player name'] = chooser.getplayer().getname(full=True)
    self.localPlayersData['effects'][account_id] = {}

old_on_player_leave = Session.on_player_leave
def on_player_leave(self, sessionplayer: ba.SessionPlayer) -> None:
    if (self.sessionmode == 'duelmode' or self.sessionmode == 'duelmode+'):
        if sessionplayer in self.duelplayers:
            self.end_duel()
    elif self.sessionmode == 'clanwar':
        if sessionplayer in self.clanwar_teams[0]:
            self.clanwar_teams[0].remove(sessionplayer)
            if len(self.clanwar_teams[0]) == 0:
                self.end_clanwar()
        elif sessionplayer in self.clanwar_teams[1]:
            self.clanwar_teams[1].remove(sessionplayer)
            if len(self.clanwar_teams[1]) == 0:
                self.end_clanwar()
    old_on_player_leave(self, sessionplayer)

old_execute_shutdown = ServerController._execute_shutdown
def new_execute_shutdown(self):
    _ba.get_foreground_host_session().update_stats()
    old_execute_shutdown(self)


Session.load_session_data = load_session_data
Session.load_stats = load_stats
Session.add_player_to_local_stats = add_player_to_local_stats
Session.update_stats = update_stats
Session.update_banlist = update_banlist
Session.kick_banned_players = kick_banned_players
Session.update_mutelist = update_mutelist
Session.update_warnlist = update_warnlist
Session.update_effects = update_effects
Session.update_allow_data = update_allow_data
Session.update_roles = update_roles
Session.load_server_data = load_server_data
Session.update_waiting_messages = update_waiting_messages
Session.show_on_screen_text = show_on_screen_text
Session.start_duel = start_duel
Session.set_duelscoretowin = set_duelscoretowin
Session.update_duel = update_duel
Session.end_duel = end_duel
Session.start_clanwar = start_clanwar
Session.set_clanwar_name_left = set_clanwar_name_left
Session.set_clanwar_name_right = set_clanwar_name_right
Session.set_clanwarscoretowin = set_clanwarscoretowin
Session.update_clanwar = update_clanwar
Session.end_clanwar = end_clanwar
Session.on_player_request = on_player_request
Session._request_player = _request_player
Session._on_player_ready = _on_player_ready
Session.on_player_leave = on_player_leave
Session._postinit = _postinit
Session.__init__ = new__init__

ServerController._execute_shutdown = new_execute_shutdown

if _ba.get_foreground_host_session():
    _ba.get_foreground_host_session()._postinit()