import random
import mongoengine

from db import Game, Player
from functions import (
    create_tournament,
    get_rankings,
    insert_game,
    insert_match,
    insert_player,
)
from mock import generate_random_matches, get_random_games, get_random_names

DB_NAME = "tournaml3"

connection = mongoengine.connect(db=DB_NAME)


def insert_mocked_players(n: int = 100) -> None:
    for name in get_random_names(n):
        insert_player(name)


def insert_mocked_games(n: int = 5) -> None:
    for game, difficulty in get_random_games(n):
        insert_game(game, difficulty)


def insert_mocked_matches(n: int = 200) -> None:
    for date, game, players_names, winner_names in generate_random_matches(n):
        insert_match(
            date=date,
            game_name=game,
            players_names=players_names,
            winners_names=winner_names,
        )


def main():
    print("Welcome to TournaML3!")
    print("Inserting mocked data!")

    insert_mocked_players(64)
    insert_mocked_games(3)
    insert_mocked_matches(1000)

    available_games = Game.objects()

    for game in available_games:
        print(get_rankings(game.name))

    print(get_rankings(None))

    available_players = Player.objects()

    teams = create_tournament(
        players_names=random.sample([p.username for p in available_players], k=64),
        n_teams=8,
    )

    for i, team in enumerate(teams):
        print(f"Team {i} is composed by: {' - '.join(team)} \n")


if __name__ == "__main__":
    connection.drop_database(DB_NAME)
    main()
