from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.shortcuts import reverse

from battlecode.stats_settings import RANKS, get_rank
from battlecode.groups import STUDENT_GROUP

from peer_review.models import Assignment
from badges.models import Badge


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )

    pts = models.IntegerField(default=0, verbose_name="Очки")

    badges = models.ManyToManyField(Badge, related_name="profiles", blank=True)
    courses = models.ManyToManyField("courses.Course", related_name="enrolled_profiles", blank=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", null=True)

    @property
    def rank(self):
        return get_rank(self.pts)

    @property
    def rank_as_str(self):
        slug = RANKS[self.rank - 1][1][7:].lower().strip()
        badge = Badge.objects.filter(slug=slug).first()
        if not badge or not badge.active:
            return "Unknown"
        return badge.name

    @property
    def total_worktime(self):
        assignments = Assignment.objects.filter(
            Q(status="success") | Q(status="failed"),
            user=self.user,
            assigned_at__isnull=False,
            completed_at__isnull=False,
        ).values("assigned_at", "completed_at")

        work_time = 0
        for item in assignments:
            assigned = item["assigned_at"]
            completed = item["completed_at"]
            if completed and assigned and completed > assigned:
                work_time += (completed - assigned).total_seconds() / 3600

        return round(work_time, 2)

    @property
    def placement(self) -> int:
        student_group = Group.objects.filter(name=STUDENT_GROUP).first()
        if not student_group:
            return 1

        student_users = student_group.user_set.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        higher_pts_count = Profile.objects.filter(
            user__in=student_users,
            pts__gt=self.pts,
        ).count()

        return higher_pts_count + 1

    def save(self, *args, **kwargs):
        if self.pts < 0:
            self.pts = 0
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_profile", args=[self.user.username])

    def __str__(self):
        return f"Profile for {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["user__username"]
