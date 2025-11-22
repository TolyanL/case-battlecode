from datetime import datetime, timedelta
from django.utils import timezone


DIFFICULTY_CHOICES = (
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard🔥"),
)

TASK_TYPE_CHOICES = (
    ("task", "Задача"),
    ("pvp", "PVP"),
)

MIN_PTS = 10

MAX_PICKED_QUESTS = 5

QUEST_BREAK_DAYS = 3


def break_delta() -> datetime:
    return timezone.now() - timedelta(days=QUEST_BREAK_DAYS)
