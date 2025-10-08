from slugify import slugify

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from battlecode.quest_settings import DIFFICULTY_CHOICES, MIN_PTS, ASSIGNMENT_STATUS_CHOICES
from .model_utils import count_quest_pts


class Quest(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название", blank=False)
    description = models.TextField(verbose_name="Описание", blank=False)
    slug = models.CharField(blank=True)

    difficulty = models.CharField(
        choices=DIFFICULTY_CHOICES,
        max_length=20,
        verbose_name="Сложность",
    )
    base_pts = models.IntegerField(verbose_name="Баллы за победу (без множителя)", default=MIN_PTS)
    penalty = models.IntegerField(verbose_name="Штраф за проигрыш", default=0)

    work_time = models.IntegerField(verbose_name="Время работы", default=3)
    check_time = models.IntegerField(verbose_name="Время проверки", default=3)

    skills = models.ManyToManyField("Skill", verbose_name="Навыки")
    language = models.ForeignKey(
        "Language",
        on_delete=models.PROTECT,
        verbose_name="Язык",
        related_name="quests",
    )
    details = models.OneToOneField(
        "QuestDetail",
        on_delete=models.CASCADE,
        verbose_name="Задачи",
    )

    active = models.BooleanField(default=True, verbose_name="Активен")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("quest_detail", kwargs={"slug": self.slug})

    # INFO: pts = base_pts + (MIN_PTS * (difficulty + (skill1_value * 0.1) + (skill2_value * 0.1) + ...))
    @property
    def pts(self) -> int:
        pts = self.base_pts + count_quest_pts(
            self.difficulty,
            list(self.skills.all()),
        )
        return pts

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"
        ordering = ["-created_at"]


class QuestDetail(models.Model):
    task = models.TextField(verbose_name="Задача")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.task

    @property
    def review_pool(self) -> list["Assignment"]:
        q = Assignment.objects.filter(quest=self, status="completed")
        if q.exists():
            return list(q.all())
        return []

    class Meta:
        verbose_name = "Квест - задача"
        verbose_name_plural = "Квесты - задачи"
        ordering = ["-created_at"]


class Language(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название", blank=False)
    slug = models.CharField(blank=True)

    active = models.BooleanField(default=True, verbose_name="Активен")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"
        ordering = ["-created_at"]


class Skill(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название", blank=False)
    slug = models.CharField(blank=True)

    #  INFO: value - вес навыка при вычислении баллов за победу в квесте
    value = models.IntegerField(verbose_name="Вес навыка", default=0)

    active = models.BooleanField(default=True, verbose_name="Активен")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["-created_at"]


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

    reviews = models.IntegerField(verbose_name="Количество проверок", default=0)
    status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS_CHOICES,
        default="active",
        verbose_name="Статус",
    )

    completed_at = models.DateTimeField(verbose_name="Дата завершения", null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата назначения")
