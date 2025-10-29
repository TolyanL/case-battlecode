from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from battlecode.quest_settings import break_delta
from battlecode.course_settings import COURSE_STATUS
from battlecode.review_settings import ASSIGNMENT_STATUS_CHOICES

from quests.models import Quest, ChecklistItem
from courses.models import Course


class Assignment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Пользователь",
    )
    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE,
        verbose_name="Квест",
        related_name="assignments",
    )

    given_pts = models.IntegerField(verbose_name="Полученные баллы", default=0)

    code = models.TextField(verbose_name="Код", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS_CHOICES,
        default="active",
        verbose_name="Статус",
    )

    completed_at = models.DateTimeField(verbose_name="Дата завершения", null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def finish(self):
        user_profile = self.user.profile
        give_pts = self.reviews_avg_pts

        self.completed_at = timezone.now()

        if give_pts > 0:
            self.status = "success"
        else:
            self.status = "failed"
            give_pts = self.quest.penalty * -1

        self.given_pts = give_pts
        user_profile.pts += give_pts

        badges = self.quest.badges.all()
        for badge in badges:
            user_profile.badges.add(badge)

        user_profile.save()
        self.save()

    def fail(self):
        user_profile = self.user.profile
        user_profile.pts += self.quest.penalty * -1

        self.status = "failed"
        self.completed_at = timezone.now()

        user_profile.save()
        self.save()

    def save(self, *args, **kwargs):
        if self.status not in ["active", "completed"]:
            give_pts = self.reviews_avg_pts
            if give_pts == 0:
                user_profile = self.user.profile
                if self.status == "failed":
                    give_pts = self.quest.penalty * -1
                    user_profile.pts += give_pts
                if self.status == "success":
                    give_pts = self.quest.pts
                    user_profile.pts += give_pts

                user_profile.save()
            self.given_pts = give_pts
        super().save(*args, **kwargs)

    @property
    def reviews(self) -> int:
        return Review.objects.filter(assignment=self).count()

    @property
    def reviews_avg_pts(self) -> int:
        values = Review.objects.filter(assignment=self).values_list("give_pts", flat=True)
        if not len(values):
            return 0
        return int(sum(values) / len(values))

    def __str__(self):
        return f"{self.user.username} - {self.quest.title}"

    class Meta:
        verbose_name = "Взятое задание"
        verbose_name_plural = "Взятые задания"
        ordering = ["-assigned_at"]


class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    status = models.CharField(
        max_length=20,
        choices=COURSE_STATUS,
        default="active",
        verbose_name="Статус",
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    @property
    def completed_quests_count(self) -> int:
        if self.course.quests.count() == 0:
            return 0

        count = (
            Assignment.objects.filter(
                user=self.user,
                quest__in=self.course.quests.all(),
                status__in=["success", "failed"],
                completed_at__gte=break_delta(),
            )
            .values("quest")
            .distinct()
            .count()
        )
        return count

    @property
    def progress_percent(self) -> int:
        total = self.course.quests.count()
        if total == 0:
            return 0

        completed = self.completed_quests_count
        return int((completed / total) * 100)

    def complete(self) -> None:
        user_profile = self.user.profile

        self.status = "success"
        self.completed_at = timezone.now()
        self.save()

        badges = self.course.badges.all()
        for badge in badges:
            user_profile.badges.add(badge)
        user_profile.save()

    def __str__(self):
        return f"{self.user.username} — {self.course.title} ({'✓' if self.completed_at else '○'})"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Прогресс по курсу"
        verbose_name_plural = "Прогресс по курсам"


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь",
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.PROTECT,
        verbose_name="Квест",
    )
    completed_tasks = models.IntegerField(default=0, verbose_name="Завершено заданий")

    grade = models.IntegerField(default=1, verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")

    give_pts = models.IntegerField(default=0, verbose_name="Баллы")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user.username} - {self.assignment.quest.title}"

    class Meta:
        verbose_name = "Ревью"
        verbose_name_plural = "Ревью"
        ordering = ["-created_at"]


class ReviewChecklistAnswer(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="checklist_answers",
        verbose_name="Ревью",
    )
    checklist_item = models.ForeignKey(
        ChecklistItem,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Пункт чек-листа",
    )

    work = models.BooleanField(
        default=False,
        verbose_name="Выполнено (Да/Нет)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ответ на пункт чек-листа"
        verbose_name_plural = "Ответы на пункты чек-листа"
        unique_together = ("review", "checklist_item")

    def __str__(self):
        return f"{self.review} — {self.checklist_item.description}: {'Да' if self.work else 'Нет'}"
