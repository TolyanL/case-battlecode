from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User, Group

from battlecode.groups import TEACHER_GROUP


@receiver(m2m_changed, sender=User.groups.through)
def set_staff_for_teachers(sender, instance, action, **kwargs):
    if action == "post_add":
        teacher_group = Group.objects.filter(name=TEACHER_GROUP).first()

        if teacher_group and teacher_group in instance.groups.all():
            if not instance.is_staff:
                instance.is_staff = True
                instance.save(update_fields=["is_staff"])
