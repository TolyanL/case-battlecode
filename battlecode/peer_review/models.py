from django.db import models
from django.contrib.auth.models import User

from battlecode.review_settings import ASSIGNMENT_STATUS_CHOICES
from quests.models import Quest, ChecklistItem


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
    )

    given_pts = models.IntegerField(verbose_name="Полученные баллы", default=0)

    code = models.TextField(verbose_name="Код")
    status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS_CHOICES,
        default="active",
        verbose_name="Статус",
    )

    @property
    def reviews(self) -> int:
        return Review.objects.filter(assignment=self).count()

    @property
    def reviews_avg_pts(self) -> int:
        values = Review.objects.filter(assignment=self).values_list("give_pts", flat=True)
        return int(sum(values) / len(values))

    completed_at = models.DateTimeField(verbose_name="Дата завершения", null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quest.title}"

    class Meta:
        verbose_name = "Взятое задание"
        verbose_name_plural = "Взятые задания"
        ordering = ["-assigned_at"]


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
