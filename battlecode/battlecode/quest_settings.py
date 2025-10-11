from datetime import datetime, timedelta


DIFFICULTY_CHOICES = (
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard🔥"),
)
ASSIGNMENT_STATUS_CHOICES = (
    ("active", "Активно"),
    ("completed", "Завершено"),
    ("failed", "Завалено"),
)

MIN_PTS = 10

MAX_PICKED_QUESTS = 3

QUEST_BREAK_DAYS = 3

break_delta = datetime.now() - timedelta(days=QUEST_BREAK_DAYS)
