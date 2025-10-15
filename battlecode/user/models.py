from django.db import models
from django.contrib.auth.models import User

from battlecode.stats_settings import RANKS
from badges.models import Badge


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

    badges = models.ManyToManyField(
        Badge,
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["user__username"]
