from datetime import datetime, timedelta
from django.utils import timezone


DIFFICULTY_CHOICES = (
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard🔥"),
)

MIN_PTS = 10

MAX_PICKED_QUESTS = 4

QUEST_BREAK_DAYS = 3


def break_delta() -> datetime:
    #     return datetime.now() - timedelta(days=QUEST_BREAK_DAYS)
    #
    #
    # def get_timestamp() -> datetime:
    return timezone.now() - timedelta(days=QUEST_BREAK_DAYS)
