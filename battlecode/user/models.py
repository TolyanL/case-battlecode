# case-battlecode/battlecode/user/models.py
from django.db import models
from django.contrib.auth.models import User
from battlecode.stats_settings import RANKS
from quests.models import Course # Импортируем Course

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
    # --- Добавленное поле для связи с курсами ---
    enrolled_courses = models.ManyToManyField(
        Course,
        related_name="enrolled_users",
        verbose_name="Записанные курсы",
        blank=True,
    )
    # --- /Добавленное поле ---

    def __str__(self):
        return f"Profile for {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["user__username"]
