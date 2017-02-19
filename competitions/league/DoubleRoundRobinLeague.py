# -*- coding: utf-8  -*-
"""Double round-robin league."""

# Copyright (C) 2014-17 Alexander Jones
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals

from . import FixtureLeague, GoalBasedTeamSeason, WinLoseDrawTeamSeason
from competitions.scheduler.roundrobin import DoubleRoundRobinScheduler


class DoubleRoundRobinLeague(FixtureLeague):

    """
    A double round-robin competition, usually a domestic league.

    This class does not recognize multi-level or divisional league structures.
    """

    def __init__(self, match_class, teams):
        """Constructor.

        @param match_class: The class of the match simulator.
        @type match_class: A Match-like object.
        @param teams: The teams competing in this league.
        @type teams: list of Team-like objects.
        """
        super(DoubleRoundRobinLeague, self).__init__(match_class=match_class,
                                                     teams=teams)
        self._schedule = DoubleRoundRobinScheduler(self._teams).generate_schedule()

    def _wrap_teams(self):
        """Wrap teams in TeamSeason objects."""
        self._teams = []
        for team in self._raw_teams:
            self._teams.append(self.TeamSeason(team))

    def play_round(self):
        """Simulate a round of matches."""
        Match = self._match_class
        round_matches = self._schedule[self.round]
        for teams in round_matches:
            match = Match(teams[0], teams[1])
            match.play()
            self._merge_stats(match)
            self._fixtures[teams] = match
        self._round += 1
        self._teams.sort(key=self.TeamSeason.key, reverse=True)

    def print_standings(self):
        """Print the league table to the console."""
        print("After Round {0}:".format(self.round))
        print(self.standings_header)
        for team in self._teams:
            print(team.standings_str())

    def print_fixtures(self):
        """Print the fixture table to the console."""
        for home in self._teams:
            for away in self._teams:
                if home == away or ((home, away) not in self._fixtures):
                    print("{:<7} ".format(" "))
                    continue
                print("{:<7} ".format(self._fixtures[(home, away)].score_str()))
            print


class AssociationFootballDoubleRoundRobinLeague(DoubleRoundRobinLeague):

    """A typical association football (football or soccer) double round-robin league."""

    standings_header = "{:<30}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}".format(
        "Team", "W", "L", "D", "Pts", "GF", "GA", "GD"
    )

    class TeamSeason(WinLoseDrawTeamSeason, GoalBasedTeamSeason):

        """An association football team season."""

        @staticmethod
        def key(x):
            """Return the sortkey for this type of object."""
            return (x.points, x.goal_diff, x.goals_for)

        @property
        def points(self):
            """Return the number of points accumulated by this team."""
            return self.wins * 3 + self.draws

        def standings_str(self):
            """Return a string to be printed in the league standings."""
            return "{:<30}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}".format(
                self, self.wins, self.losses, self.draws, self.points,
                self.goals_for, self.goals_against, self.goal_diff
            )

    def _merge_stats(self, match):
        """Merge the match stats into the TeamSeason objects."""
        team1 = match.team1
        team2 = match.team2
        if match.drawn:
            team1.drew()
            team2.drew()
        else:
            match.winner.won()
            match.loser.lost()
        team1.scored(match.score1)
        team2.allowed(match.score1)
        team2.scored(match.score2)
        team1.allowed(match.score2)
