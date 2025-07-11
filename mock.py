from datetime import datetime
import random
import string

from db import Game, Player
from enums import Difficulty


def get_random_names(n: int = 100) -> list[str]:
    return ["".join(random.choices(string.ascii_lowercase, k=8)) for _ in range(n)]


def get_random_games(n: int = 5) -> list[tuple[str, Difficulty]]:
    games = [
        (
            "Biliardino",
            Difficulty.EASY,
        ),
        (
            "FIFA",
            Difficulty.EASY,
        ),
        (
            "Foglie",
            Difficulty.HARD,
        ),
        (
            "Crack List",
            Difficulty.EASY,
        ),
        (
            "Tranquility",
            Difficulty.HARD,
        ),
        (
            "Concept",
            Difficulty.EASY,
        ),
        (
            "Carcassonne",
            Difficulty.EASY,
        ),
    ]
    return random.sample(games, k=n)


def generate_random_matches(n: int) -> list[datetime, str, list[str], list[str]]:
    matches = []

    games = Game.objects()
    players = Player.objects()

    for _ in range(n):
        if random.random() > 0.5:
            player_per_team = 1
        else:
            player_per_team = 2

        game_players = [
            p.username for p in random.choices(players, k=player_per_team * 2)
        ]

        matches.append(
            (
                datetime.today(),
                random.choice(games).name,
                game_players,
                random.choices(game_players, k=player_per_team),
            )
        )

    return matches

    
