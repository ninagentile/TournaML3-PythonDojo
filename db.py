from datetime import datetime, timedelta
from typing import Any
from bson import ObjectId
from mongoengine import PULL, ValidationError
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import (
    Document,
    DynamicDocument,
    DynamicEmbeddedDocument,
    EmbeddedDocument,
)
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    DictField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    EnumField,
    FloatField,
    IntField,
    LazyReferenceField,
    ListField,
    MapField,
    StringField,
)

from enums import Difficulty


class Player(Document):
    username: str = StringField()


class Game(Document):
    name: str = StringField()
    difficulty: Difficulty = EnumField(Difficulty)


class Match(Document):
    date: str = DateTimeField()
    game: Game = LazyReferenceField(Game)
    players: list[Player] = ListField(
        LazyReferenceField(
            Player,
            passthrough=True,
        )
    )
    winners: list[Player] = ListField(
        LazyReferenceField(
            Player,
            passthrough=True,
        )
    )
