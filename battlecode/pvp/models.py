from secrets import token_hex
from datetime import timedelta

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

from battlecode.pvp_settings import ASSIGNMENT_STATUS_CHOICES
from quests.models import Quest


class PvpAssignment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pvp_assignments",
        verbose_name="Пользователь",
    )
    battle = models.ForeignKey(
        "Battle",
        on_delete=models.PROTECT,
        verbose_name="Бой",
        related_name="pvp_assignments",
    )
    opponent = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Оппонент",
    )

    status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS_CHOICES,
        default="active",
        verbose_name="Статус",
    )

    code = models.TextField(
        null=True,
        blank=True,
        verbose_name="Решение пользователя",
    )
    is_ready = models.BooleanField(default=False, verbose_name="Готов")

    given_pts = models.IntegerField(verbose_name="Полученные баллы", default=0)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def finish(self):
        self.status = "success"
        self.user.profile.pts += self.battle.quest.pts
        self.save()

    def complete(self):
        self.status = "completed"
        self.save()

    def skip(self):
        self.status = "skiped"
        self.save()

    def self_fail(self):
        self.status = "failed"
        self.user.profile.pts += self.battle.quest.penalty * -1
        self.user.profile.save()
        self.save()

    @property
    def deadline(self):
        return self.created_at + timedelta(hours=self.battle.quest.work_time)

    def fail(self, id: int):
        self.status = "failed"

        if self.user.id == id:
            self.user.profile.pts += self.battle.quest.penalty * -1
            self.user.profile.save()
        else:
            self.opponent.profile.pts += self.battle.quest.penalty * -1
            self.opponent.profile.save()

        self.save()

    def __str__(self):
        return f"PVP {self.user.username} vs {self.opponent.username} in {self.battle.quest.title}"

    class Meta:
        verbose_name = "PVP задание"
        verbose_name_plural = "PVP задания"
        ordering = ["-created_at"]


class Battle(models.Model):
    code = models.CharField(max_length=100, blank=True, unique=True, verbose_name="Код")
    started = models.BooleanField(default=False, verbose_name="Запущено")

    quest = models.ForeignKey(
        Quest,
        on_delete=models.PROTECT,
        verbose_name="Квест",
        related_name="pvp_battles",
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def start(self):
        self.started = True
        self.save()

    def get_absolute_url(self) -> str:
        return reverse("pvp_battle", kwargs={"code": self.code})

    def save(self, *args, **kwargs):
        if not len(self.code):
            self.code = token_hex(4).upper()
        super().save(*args, **kwargs)
