from django.db import models
from django.contrib.auth.models import User

from battlecode.review_settings import ASSIGNMENT_STATUS_CHOICES
from quests.models import Quest


class PvpAssignment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pvp",
        verbose_name="Пользователь",
    )
    quest = models.ForeignKey(
        Quest,
        on_delete=models.PROTECT,
        verbose_name="Квест",
        related_name="pvp_assignments",
    )

    status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS_CHOICES,
        default="active",
        verbose_name="Статус",
    )

    given_pts = models.IntegerField(verbose_name="Полученные баллы", default=0)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"PVP {self.user.username} - {self.quest.title}"

    class Meta:
        verbose_name = "PVP задание"
        verbose_name_plural = "PVP задания"
        ordering = ["-created_at"]
