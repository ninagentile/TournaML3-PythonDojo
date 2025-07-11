from db import Game, Match, Player
from mongoengine import DoesNotExist
from datetime import datetime


class MatchQueries:
    def get_matches_by_date_range(
        from_date: str | None, to_date: str | None, game_name: str | None
    ) -> list[Match]:
        if to_date is None:
            to_date = datetime.now().date().isoformat()

        if from_date is None:
            matches_in_date_range: list[Match] = Match.objects()
        else:
            matches_in_date_range: list[Match] = Match.objects.filter(
                date__gte=from_date, date__lte=to_date
            )

        if game_name is None:
            return matches_in_date_range
        else:
            return [m for m in matches_in_date_range if m.game.fetch().name == game_name]


class PlayerQueries:
    def get_by_name(player_name: str) -> Player:
        return Player.objects.get(username=player_name)


class GameQueries:
    def get_by_name(name: str) -> Game:
        # Get the game from DB
        try:
            return Game.objects.get(name=name)
        except DoesNotExist:
            raise ValueError("Game doesn't exist!")
