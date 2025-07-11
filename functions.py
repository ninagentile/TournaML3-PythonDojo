from datetime import datetime
import random
from db import Game, Match, Player
from enums import Difficulty
from mongoengine import DoesNotExist
from queries import PlayerQueries, MatchQueries, GameQueries
from collections import defaultdict
import polars as pl


def insert_player(username: str) -> None:
    """
    Create a player with the given username
    """

    n_players = Player.objects(username=username)

    if n_players:
        raise ValueError("Username already exists!")

    Player(username=username).save()


def insert_game(name: str, difficulty: Difficulty) -> None:
    """
    Create a player with the given username
    """

    n_games = Game.objects(name=name)

    if n_games:
        raise ValueError("Game already exists!")

    Game(name=name, difficulty=difficulty).save()


def insert_match(
    date: datetime, game_name: str, players_names: list[str], winners_names: list[str]
) -> None:
    """
    Create a match
    """
    # Get the game from DB
    game = GameQueries.get_by_name(game_name)

    # Get the players
    players = []
    for p in players_names:
        try:
            player = PlayerQueries.get_by_name(p)
            players.append(player)
        except DoesNotExist:
            raise ValueError(f"The player named {p} does not exist in DB")

    # Get the winners
    winners = []
    for w in winners_names:
        try:
            player = PlayerQueries.get_by_name(w)
            winners.append(player)
        except DoesNotExist:
            raise ValueError(f"The player named {p} does not exist in DB")

    # Create Match
    match = Match(game=game, players=players, winners=winners, date=date).save()

    return match


def get_rankings(game: str | None) -> pl.DataFrame:
    results = defaultdict(list)

    players = Player.objects()

    matches = MatchQueries.get_matches_by_date_range(
        game_name=game, from_date=None, to_date=None
    )

    for player in players:
        results["Player Name"].append(player.username)

        n_played_matches = sum(
            1 if str(player.id) in [str(m.id) for m in match.players] else 0
            for match in matches
        )

        n_won_matches = sum(
            1 if str(player.id) in [str(m.id) for m in match.winners] else 0
            for match in matches
        )

        results["Won"].append(n_won_matches)
        results["Played"].append(n_played_matches)
        results["Elo"].append(
            n_won_matches * get_score(matches[0].game.fetch())
            - (n_played_matches - n_won_matches)
        )

    df = pl.DataFrame(results).sort("Won", descending=True)

    df.write_csv(f"{game if game else 'Overall'}.csv")

    return df


def get_score(game: Game) -> int:
    return 1 * game.difficulty.value


def create_ranking(from_date: str | None, to_date: str | None, game_name: str | None):
    # Get matches
    matches = MatchQueries.get_matches_by_date_range(
        from_date=from_date, to_date=to_date, game_name=game_name
    )

    # for each game get the point for each player
    scores_by_username = defaultdict(int)
    for match in matches:
        for winner in match.winners:
            score = get_score(match.game)
            player_name = winner.name
            scores_by_username[player_name] += score

    # Order scores and return them
    return dict(sorted(scores_by_username.items(), key=lambda item: -item[1]))


def create_tournament(players_names: list[str], n_teams: int):
    if n_teams == 0:
        return ValueError("n_teams cannot be 0")

    if n_teams > len(players_names):
        return ValueError("n_teams cannot be greater than the number of players")

    if len(players_names) % n_teams != 0:
        return ValueError("There are teams with a different number of players")

    n_players_per_team = len(players_names) // n_teams

    teams: list[list[str]] = []
    
    while len(players_names):
        team = []
        for _ in range(n_players_per_team):
            extracted_player = random.choice(players_names)
            team.append(extracted_player)
            players_names.remove(extracted_player)
        teams.append(team)

    return teams
