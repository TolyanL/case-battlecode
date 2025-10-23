# battlecode/user/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile

@receiver(post_save, sender=User)
def create_profile_and_assign_student_role(sender, instance, created, **kwargs):
    if created:
        # Создаём Profile (если ещё не создан)
        Profile.objects.get_or_create(user=instance)

        # Назначаем группу "Students"
        students_group, _ = Group.objects.get_or_create(name="Students")
        instance.groups.add(students_group)