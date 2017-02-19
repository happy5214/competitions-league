# -*- coding: utf-8  -*-
"""League package."""

# Copyright (C) 2017 Alexander Jones
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

from __future__ import unicode_literals

from competitions.match import Match


class League(object):

    """A generic league-style competition."""

    def __init__(self, match_class=Match, teams=[]):
        """Constructor."""
        self._raw_teams = teams
        self._wrap_teams()
        self._round = 0
        self._match_class = match_class

    @property
    def round(self):
        """Return the current round."""
        return self._round

    def _wrap_teams(self):
        """Wrap team objects in TeamSeason objects."""
        raise NotImplementedError

    def _merge_stats(self, match):
        """Merge match stats into the TeamSeason objects."""
        raise NotImplementedError

    def play_round(self):
        """Simulate a round of matches."""
        raise NotImplementedError

    def play_season(self):
        """Simulate the entire league season."""
        try:
            while True:
                self.play_round()
        except IndexError:
            return self._teams[0]

    def print_standings(self):
        """Print the league table/standings to the console."""
        raise NotImplementedError


class FixtureLeague(League):

    """A league with printable fixtures."""

    def __init__(self, match_class, teams):
        """Constructor.

        @param match_class: The class of the match simulator.
        @type match_class: A Match-like object.
        @param teams: The teams competing in this league.
        @type teams: list of Team-like objects.
        """
        super(FixtureLeague, self).__init__(match_class=match_class,
                                            teams=teams)
        self._fixtures = {}

    def print_fixtures(self):
        """Print the fixture table to the console."""
        raise NotImplementedError


class TeamSeason(object):

    """A team's participation in a league."""

    def __init__(self, team):
        """Constructor.

        @param team: The team competing in the league.
        @type team: Team-like object.
        """
        self._team = team

    def __str__(self):
        """Return a str representation of the team's season.

        This simply returns the str version of the team.

        @return: The team's season as a str
        @rtype: str
        """
        return str(self._team)

    @property
    def team(self):
        """Return the team competing in the league."""
        return self._team

    @property
    def key(self):
        """Return the sortkey for this type of team."""
        raise NotImplementedError

    @property
    def standings_str(self):
        """Return a string to be printed as part of the league standings."""
        raise NotImplementedError


class WinLoseDrawTeamSeason(TeamSeason):

    """A TeamSeason based on wins, losses, and draws."""

    def __init__(self, team):
        """Constructor."""
        super(WinLoseDrawTeamSeason, self).__init__(team)
        self._wins = 0
        self._losses = 0
        self._draws = 0

    @property
    def wins(self):
        """Return the number of wins for this team in this league."""
        return self._wins

    @property
    def losses(self):
        """Return the number of losses for this team in this league."""
        return self._losses

    @property
    def draws(self):
        """Return the number of draws for this team in this league."""
        return self._draws

    def won(self):
        """Increment this team's win count."""
        self._wins += 1

    def lost(self):
        """Increment this team's loss count."""
        self._losses += 1

    def drew(self):
        """Increment this team's draw count."""
        self._draws += 1


class GoalBasedTeamSeason(TeamSeason):

    """A TeamSeason based on goals (use PointBasedTeamSeason if points are used)."""

    def __init__(self, team):
        """Constructor."""
        super(GoalBasedTeamSeason, self).__init__(team)
        self._goals_for = 0
        self._goals_against = 0

    @property
    def goals_for(self):
        """Return the number of goals scored by this team."""
        return self._goals_for

    @property
    def goals_against(self):
        """Return the number of goals allowed by this team."""
        return self._goals_against

    @property
    def goal_diff(self):
        """Return this team's goal differential."""
        return self._goals_for - self._goals_against

    def scored(self, goals):
        """Add scored goals to this team's stats."""
        self._goals_for += goals

    def allowed(self, goals):
        """Add allowed goals to this team's stats."""
        self._goals_against += goals
