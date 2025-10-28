from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User, Group

from battlecode.groups import ADMIN_GROUP, TEACHER_GROUP, STUDENT_GROUP


@receiver(m2m_changed, sender=User.groups.through)
def set_group_permissions(sender, instance, action, **kwargs):
    if action not in ("post_add", "post_remove", "post_clear"):
        return

    student_group = Group.objects.filter(name=STUDENT_GROUP).first()
    admin_group = Group.objects.filter(name=ADMIN_GROUP).first()
    teacher_group = Group.objects.filter(name=TEACHER_GROUP).first()

    if all([student_group, admin_group, teacher_group]):
        is_staff = False
        is_superuser = False

        user_groups = set(instance.groups.all())

        if admin_group in user_groups:
            is_superuser = True
            is_staff = True
        elif teacher_group in user_groups:
            is_staff = True

        if instance.is_staff != is_staff or instance.is_superuser != is_superuser:
            instance.is_staff = is_staff
            instance.is_superuser = is_superuser
            instance.save(update_fields=["is_staff", "is_superuser"])
