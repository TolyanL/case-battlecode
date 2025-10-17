from slugify import slugify

from django.db import models
from django.urls import reverse

from colorfield.fields import ColorField

from battlecode.quest_settings import DIFFICULTY_CHOICES, MIN_PTS
from .model_utils import count_quest_pts, get_contrast_color


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
    checklist = models.OneToOneField(
        "QuestReviewChecklist",
        on_delete=models.PROTECT,
        verbose_name="Чек-лист ревью квеста",
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

    class Meta:
        verbose_name = "Квест - задача"
        verbose_name_plural = "Квесты - задачи"
        ordering = ["-created_at"]


class Language(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название", blank=False)
    slug = models.CharField(blank=True)

    color = ColorField(format="hex", default="#000000", verbose_name="Цвет")

    active = models.BooleanField(default=True, verbose_name="Активен")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def text_color(self):
        return get_contrast_color(self.color)

    @property
    def bg_color(self):
        hex_color = self.color.lstrip("#")
        alpha = 0.2
        r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, {alpha})"

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


class QuestReviewChecklist(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Чек-лист ревью квеста"
        verbose_name_plural = "Чек-листы ревью квеста"
        ordering = ["-created_at"]


class ChecklistItem(models.Model):
    review = models.ForeignKey(
        QuestReviewChecklist,
        on_delete=models.CASCADE,
        related_name="checklist_items",
        verbose_name="Чек-лист Ревью",
    )
    slug = models.CharField(null=True, blank=True)
    description = models.CharField(max_length=500, verbose_name="Описание пункта")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Элемент чеклиста"
        verbose_name_plural = "Элементы чеклиста"
        ordering = ["-created_at"]
