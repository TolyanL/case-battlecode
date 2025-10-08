from django.db import models

from quests.models import Assignment


class Review(models.Model):
    user = models.ForeignKey(
        "user.Profile",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь",
    )
    quest = models.ForeignKey(
        Assignment,
        on_delete=models.PROTECT,
        verbose_name="Квест",
    )
    grade = models.IntegerField(default=1, verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    @property
    def quest_user(self):
        return self.quest.user

    def __str__(self):
        return f"{self.user.username} - {self.quest.title}"

    class Meta:
        verbose_name = "Ревью"
        verbose_name_plural = "Ревью"
        ordering = ["-created_at"]
