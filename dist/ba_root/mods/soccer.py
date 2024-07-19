# Released under the MIT License. See LICENSE for details.
#
"""Hockey game and support classes."""

# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import random

import _ba, ba
from ba._general import Call, WeakCall
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.scoreboard import Scoreboard
from bastd.actor.powerupbox import PowerupBoxFactory
from bastd.gameutils import SharedObjects

from actors.ball import Ball, getBallMaterial
from actors.freeze_box import FreezeBox, FreezeBoxSpawner
from actors.hologram import Hologram, getHologramMaterial

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, Union

# Определяем основные классы игры

class BallDiedMessage:
    """Сообщение о том, что мяч умер."""
    def __init__(self, ball: SoccerBall):
        self.ball = ball

class SoccerBall(Ball):

    def __init__(self,
                 size: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0)):
        ba.Actor.__init__(self)
        shared = SharedObjects.get()
        activity = self.getactivity()

        self._spawn_pos = (0.0, 0.4, random.uniform(-4.0, 4.0))
        # Спауним мяч немного выше указанной точки.
        self.scored = False
        assert activity is not None

        # Получаем материалы для мяча
        ball_material = getBallMaterial()
        ball_material.add_actions(actions=('call', 'at_connect', self.handle_hit))
        bmats = [shared.object_material, ball_material, activity.soccer_ball_material]

        # Создаем узел мяча
        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': ba.getmodel('frostyPelvis'),
                                   'color_texture': ba.gettexture('aliBSRemoteIOSQR'),
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'reflection_scale': [0.1],
                                   'shadow_size': 0.2,
                                   'is_area_of_interest': True,
                                   'position': self._spawn_pos,
                                   'materials': bmats,
                                   'body_scale': 1.0,
                                   'density': 1.24,
                               })
        # Анимируем масштаб модели мяча
        ba.animate(self.node, 'model_scale', {0: 0, 0.2: 1.0 * 1.3 * 0.9, 0.26: 1.0 * 1.0 * 0.9})
        self.owner = None

        self.last_players_to_touch: dict[int, Player] = {}
        self.last_player_to_touch = None
        self.last_player_to_assist = None
        self.scored = False

    def handlemessage(self, msg: Any) -> Any:

        if isinstance(msg, ba.DieMessage):
            super().handlemessage(ba.DieMessage())
            activity = self._activity()
            if activity and not msg.immediate:
                activity.handlemessage(BallDiedMessage(self))

        # Если мяч выходит за границы, перемещаем его обратно в исходную точку.
        if isinstance(msg, ba.OutOfBoundsMessage):
            if self.node.position[1] < 4.0:
                self.node.position = self._spawn_pos
                self.node.velocity = (0.0, 7.0, 0.0)

        elif isinstance(msg, ba.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1],
                msg.force_direction[2])

            # Если удар пришел от игрока, записываем его как последнего, кто касался мяча.
            s_player = msg.get_source_player(Player)
            if s_player is not None:
                activity = self._activity()
                if activity:
                    if s_player in activity.players:
                        self.last_players_to_touch[s_player.team.id] = s_player
                        if self.last_player_to_touch != s_player:
                            self.last_player_to_assist = self.last_player_to_touch
                            self.last_player_to_touch = s_player

        else:
            super().handlemessage(msg)


class Player(ba.Player['Team']):
    """Тип игрока для нашей игры."""


class Team(ba.Team[Player]):
    """Тип команды для нашей игры."""

    def __init__(self) -> None:
        self.score = 0


# ba_meta export game
class SoccerGame(ba.TeamGameActivity[Player, Team]):
    """Игра в хоккей."""

    name = 'Soccer'
    description = 'Забивайте голы.'
    available_settings = [
        ba.IntSetting(
            'Score to Win',
            min_value=1,
            default=1,
            increment=1,
        ),
        ba.IntChoiceSetting(
            'Time Limit',
            choices=[
                ('None', 0),
                ('1 Minute', 60),
                ('2 Minutes', 120),
                ('5 Minutes', 300),
                ('10 Minutes', 600),
                ('20 Minutes', 1200),
            ],
            default=0,
        ),
        ba.FloatChoiceSetting(
            'Respawn Times',
            choices=[
                ('Shorter', 0.25),
                ('Short', 0.5),
                ('Normal', 1.0),
                ('Long', 2.0),
                ('Longer', 4.0),
            ],
            default=1.0,
        ),
    ]
    default_music = ba.MusicType.HOCKEY

    @classmethod
    def supports_session_type(cls, sessiontype: type[ba.Session]) -> bool:
        return issubclass(sessiontype, ba.DualTeamSession)

    @classmethod
    def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
        return ba.getmaps('hockey')

    def __init__(self, settings: dict):
        super().__init__(settings)

        shared = SharedObjects.get()
        self._scoreboard = Scoreboard()
        self._cheer_sound = ba.getsound('cheer')
        self._chant_sound = ba.getsound('crowdChant')
        self._foghorn_sound = ba.getsound('foghorn')
        self._swipsound = ba.getsound('swip')
        self._whistle_sound = ba.getsound('refWhistle')
        self._ball_spawn_pos: Optional[Sequence[float]] = None
        self._score_regions: Optional[list[ba.NodeActor]] = None
        self._ball: Optional[SoccerBall] = None
        self._score_to_win = int(settings['Score to Win'])
        self._time_limit = float(settings['Time Limit'])

        self.slow_motion = True
        self._ice_floor = False

    def get_instance_description(self) -> Union[str, Sequence]:
        if self._score_to_win == 1:
            return 'Score a goal.'
        return 'Score ${ARG1} goals.', self._score_to_win

    def get_instance_description_short(self) -> Union[str, Sequence]:
        if self._score_to_win == 1:
            return 'score a goal'
        return 'score ${ARG1} goals', self._score_to_win

    def on_transition_in(self) -> None:
        super().on_transition_in()
        shared = SharedObjects.get()
        activity = ba.getactivity()
        activity.map.floor.color = (0.2, 1.0, 0.2)
        self.map.is_hockey = False
        activity.map.node.materials = [shared.footing_material]
        activity.map.floor.materials = [shared.footing_material]
        self.map.stands.color_texture = ba.gettexture('fontExtras3')

    def on_begin(self) -> None:
        super().on_begin()

        shared = SharedObjects.get()
        self.soccer_ball_material = ba.Material()
        # Отслеживаем, какой игрок последний касался мяча
        self.soccer_ball_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(('call', 'at_connect',
                      self._handle_ball_player_collide), ))

        # Мы хотим, чтобы мяч уничтожал пауэрупы, а не застревал на них
        self.soccer_ball_material.add_actions(
            conditions=('they_have_material',
                        PowerupBoxFactory.get().powerup_material),
            actions=(('modify_part_collision', 'physical', False),
                     ('message', 'their_node', 'at_connect', ba.DieMessage())))
        self._score_region_material = ba.Material()
        self._score_region_material.add_actions(
            conditions=('they_have_material', self.soccer_ball_material),
            actions=(('modify_part_collision', 'collide',
                      True), ('modify_part_collision', 'physical', False),
                     ('call', 'at_connect', self._handle_score)))

        self.setup_standard_time_limit(self._time_limit)
        self.setup_standard_powerup_drops()
        self._ball_spawn_pos = self.map.get_flag_position(None)
        self._spawn_ball()

        # Устанавливаем две зоны для заброса
        defs = self.map.defs
        self._score_regions = []
        self._score_regions.append(
            ba.NodeActor(
                ba.newnode('region',
                           attrs={
                               'position': defs.boxes['goal1'][0:3],
                               'scale': defs.boxes['goal1'][6:9],
                               'type': 'box',
                               'materials': [self._score_region_material]
                           })))
        self._score_regions.append(
            ba.NodeActor(
                ba.newnode('region',
                           attrs={
                               'position': defs.boxes['goal2'][0:3],
                               'scale': defs.boxes['goal2'][6:9],
                               'type': 'box',
                               'materials': [self._score_region_material]
                           })))
        self._update_scoreboard()
        ba.playsound(self._chant_sound)

    def on_team_join(self, team: Team) -> None:
        self._update_scoreboard()

    def _handle_ball_player_collide(self) -> None:
        collision = ba.getcollision()
        try:
            ball = collision.sourcenode.getdelegate(SoccerBall, True)
            player = collision.opposingnode.getdelegate(PlayerSpaz,
                                                        True).getplayer(
                                                            Player, True)
        except ba.NotFoundError:
            return

        ball.last_players_to_touch[player.team.id] = player
        if ball.last_player_to_touch != player:
            ball.last_player_to_assist = ball.last_player_to_touch
            ball.last_player_to_touch = player

    def _kill_ball(self) -> None:
        self._ball.handlemessage(ba.DieMessage())

    def _handle_score(self) -> None:
        """Одно очко было забито."""

        assert self._ball is not None
        assert self._score_regions is not None

        # Мяч может оставаться на поле еще некоторое время,
        # поэтому мы не хотим, чтобы он мог забить еще раз.
        if self._ball.scored:
            return

        region = ba.getcollision().sourcenode
        index = 0
        for index, score_region in enumerate(self._score_regions):
            if region == score_region.node:
                break

        for team in self.teams:
            if team.id == index:
                scoring_team = team
                team.score += 1

                # Уведомляем всех игроков о праздновании.
                for player in team.players:
                    if player.actor:
                        player.actor.handlemessage(ba.CelebrateMessage(2.0))

                # Если у нас есть игрок из забившей команды, который последний касался нас,
                # даем им очки.
                if (scoring_team.id in self._ball.last_players_to_touch
                        and self._ball.last_players_to_touch[scoring_team.id]):
                    self.stats.player_scored(
                        self._ball.last_players_to_touch[scoring_team.id],
                        100,
                        big_message=True)

                scoring_player = self._ball.last_player_to_touch
                assisting_player = self._ball.last_player_to_assist
                try:
                    if scoring_player is not None:
                        session = self.session
                        from ModData.account_info import client_to_account
                        from ModData import stats

                        if scoring_player in scoring_team.players:
                            account_id = client_to_account(scoring_player.sessionplayer.inputdevice.client_id)
                            stats.increase_value(session.localPlayersData['stats'], account_id, 'goals')
                            if assisting_player is not None and assisting_player in scoring_team.players:
                                account_id = client_to_account(assisting_player.sessionplayer.inputdevice.client_id)
                                stats.increase_value(session.localPlayersData['stats'], account_id, 'assists')
                        else:
                            account_id = client_to_account(scoring_player.sessionplayer.inputdevice.client_id)
                            stats.increase_value(session.localPlayersData['stats'], account_id, 'autogoals')
                except:
                    pass

                # Заканчиваем игру, если мы выиграли.
                if team.score >= self._score_to_win:
                    self.end_game()

        ba.playsound(self._foghorn_sound)
        ba.playsound(self._cheer_sound)

        self._ball.scored = True

        # Убиваем мяч (он сам переспавнится через некоторое время).
        ba.timer(1.0, self._kill_ball)

        light = ba.newnode('light',
                           attrs={
                               'position': ba.getcollision().position,
                               'height_attenuated': False,
                               'color': (1, 0, 0)
                           })
        ba.animate(light, 'intensity', {0: 0, 0.5: 1, 1.0: 0}, loop=True)
        ba.timer(1.0, light.delete)

        ba.cameraflash(duration=10.0)
        self._update_scoreboard()

    def end_game(self) -> None:
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)

    def _update_scoreboard(self) -> None:
        winscore = self._score_to_win
        for team in self.teams:
            self._scoreboard.set_team_value(team, team.score, winscore)

    def handlemessage(self, msg: Any) -> Any:

        # Респауним мертвых игроков, если они все еще в игре.
        if isinstance(msg, ba.PlayerDiedMessage):
            # Добавляем стандартное поведение...
            super().handlemessage(msg)
            self.respawn_player(msg.getplayer(Player))

        # Респауним мертвые мячи.
        elif isinstance(msg, BallDiedMessage):
            if not self.has_ended():
                ba.timer(3.0, self._spawn_ball)
        else:
            super().handlemessage(msg)

    def spawn_player_spaz(self,
                          player: PlayerType,
                          position: Sequence[float] = (0, 0, 0),
                          angle: float = None) -> PlayerSpaz:
        super().spawn_player_spaz(player)
        player.actor.equip_boxing_gloves()

    def _flash_ball_spawn(self) -> None:
        light = ba.newnode('light',
                           attrs={
                               'position': self._ball_spawn_pos,
                               'height_attenuated': False,
                               'color': (1, 0, 0)
                           })
        ba.animate(light, 'intensity', {0.0: 0, 0.25: 1, 0.5: 0}, loop=True)
        ba.timer(1.0, light.delete)

    def _spawn_ball(self) -> None:
        ba.playsound(self._swipsound)
        ba.playsound(self._whistle_sound)
        assert self._ball_spawn_pos is not None
        self._ball = SoccerBall(position=self._ball_spawn_pos).autoretain()

    def _standard_drop_powerup(self, index: int, expire: bool = True) -> None:
        # pylint: disable=cyclic-import
        from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory
        PowerupBox(
            position=[(-11.0, 1.080990833, 0.0), (11.0, 1.080990833, 0.0)][index],
            poweruptype='health',
            expire=expire).autoretain()

    def _standard_drop_powerups(self) -> None:
        """Стандартный выпадение пауэрупов."""

        # Выпадает по одному пауэрупу на очко.
        for i in range(2):
            _ba.timer(i * 0.4, WeakCall(self._standard_drop_powerup, i))

    def _setup_standard_tnt_drops(self) -> None:
        """Стандартный выпадение динамита."""
        # pylint: disable=cyclic-import
        for i, point in enumerate(self.map.tnt_points):
            assert self._tnt_spawners is not None
            if self._tnt_spawners.get(i) is None:
                self._tnt_spawners[i] = FreezeBoxSpawner(point)

# ba_meta export plugin
class SoccerPlugin(ba.Plugin):
    def on_app_launch(self) -> None:
        pass
