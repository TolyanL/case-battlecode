from slugify import slugify

from django.db import models
from colorfield.fields import ColorField

from quests.model_utils import get_contrast_color
from quests.models import Quest
from courses.models import Course


class Badge(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    slug = models.CharField(max_length=100, blank=True, unique=True)

    description = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    color = ColorField(
        format="hex",
        default="#000000",
        verbose_name="Цвет",
    )

    rel_quests = models.ManyToManyField(Quest, related_name="badges", blank=True)
    rel_courses = models.ManyToManyField(Course, related_name="badges", blank=True)

    active = models.BooleanField(default=True, verbose_name="Активен")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        if self.slug == "":
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
