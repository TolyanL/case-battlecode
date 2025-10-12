# case-battlecode/battlecode/user/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created: # Если пользователь только что создан
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'): # Проверяем, есть ли у пользователя профиль
        instance.profile.save() # Сохраняем его (на всякий случай)

# Примечание: Нужно убедиться, что сигналы подгружаются.
# Это часто делается в apps.py.