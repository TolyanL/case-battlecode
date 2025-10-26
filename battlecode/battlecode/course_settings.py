from datetime import datetime, timedelta
from django.utils import timezone


from .quest_settings import QUEST_BREAK_DAYS

COURSE_BREAK_DELTA = QUEST_BREAK_DAYS * 2

COURSE_STATUS = (
    ("active", "Активный"),
    ("failed", "Заваленный"),
    ("success", "Завершенный"),
)


def break_delta() -> datetime:
    return timezone.now() - timedelta(days=COURSE_BREAK_DELTA)
