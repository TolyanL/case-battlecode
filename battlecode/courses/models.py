from django.db import models
from quests.models import Quest


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class CourseQuest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="course_quests")
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, verbose_name="Квест")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок в курсе")

    def __str__(self):
        return f"{self.course.title} - {self.quest.title}"

    class Meta:
        verbose_name = "Квест в курсе"
        verbose_name_plural = "Квесты в курсе"
        ordering = ["order"]

