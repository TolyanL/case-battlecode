from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

from battlecode.stats_settings import RANKS

from peer_review.models import Assignment
from badges.models import Badge


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )

    rank = models.IntegerField(default=1, verbose_name="Ранг", choices=RANKS)
    pts = models.IntegerField(default=0, verbose_name="Очки")

    badges = models.ManyToManyField(Badge, blank=True)
    courses = models.ManyToManyField("courses.Course", related_name="enrolled_profiles", blank=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", null=True)

    @property
    def total_worktime(self):
        assignments = Assignment.objects.filter(
            Q(status="success") | Q(status="failed"),
            user=self.user,
        ).values("assigned_at", "completed_at")

        work_time = 0
        for item in assignments:
            work_time += (item["completed_at"] - item["assigned_at"]).total_seconds() / 3600

        return round(work_time, 2)

    def __str__(self):
        return f"Profile for {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["user__username"]
