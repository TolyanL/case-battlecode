from django.db import models
from django.contrib.auth.models import User

from battlecode.stats_settings import RANKS


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    rank = models.IntegerField(
        default=1,
        verbose_name="Ранг",
        choices=RANKS,
    )
    pts = models.IntegerField(default=0, verbose_name="Очки")
