from django.db import models

class Quest(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название", blank=False, validators=[MinLengthValidator(3)])
    description = models.TextField(verbose_name="Описание", blank=False)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        status = " (Активен)" if self.is_active else " (Неактивен)"
        return f"{self.title}{status}"
    
    # Не факт что будет использоваться, но пусть пока будет
    def get_absolute_url(self):
        """Возвращает URL для просмотра деталей квеста."""
        # 'quests:quest_detail' - это имя URL, которое будет определено в 3-м пункте
        # kwargs={'pk': self.pk} передаёт первичный ключ (ID) квеста
        return reverse('quests:quest_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"
        ordering = ['-created_at']