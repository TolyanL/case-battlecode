from slugify import slugify

from colorfield.fields import ColorField
from django.db import models

from quests.models import Quest


class Badge(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.CharField(max_length=100, blank=True)

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

    rel_quests = models.ManyToManyField(Quest, related_name="rel_badges", blank=True, null=True)

    active = models.BooleanField(default=True, verbose_name="Активен")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
