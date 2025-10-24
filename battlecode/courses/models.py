from slugify import slugify

from django.db import models
from django.db.models.aggregates import Sum

from django.urls import reverse

from quests.models import Quest, Skill


class Course(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание", blank=True)
    slug = models.CharField(max_length=200, blank=True)

    quests = models.ManyToManyField(Quest, through="CourseQuest", related_name="courses")

    active = models.BooleanField(default=True, verbose_name="Активный")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    @property
    def quest_count(self):
        return self.quests.count()

    @property
    def skills(self):
        return Skill.objects.filter(quests__courses=self).distinct()

    @property
    def total_pts(self):
        q = self.quests.all()
        return sum([q.pts for q in q])

    @property
    def work_time(self):
        return self.quests.aggregate(Sum("work_time"))["work_time__sum"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class CourseQuest(models.Model):
    course = models.ForeignKey("Course", related_name="course_quests", on_delete=models.CASCADE)

    quest = models.ForeignKey(Quest, related_name="course_quests", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.order}. {self.quest.title}"

    class Meta:
        ordering = ["order"]
        unique_together = ("course", "quest")
