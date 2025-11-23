from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from pvp.models import PvpAssignment

from logging import getLogger


logger = getLogger(__name__)


@shared_task()
def check_pvp_assignments() -> None:
    return
    items = PvpAssignment.objects.filter(status="active").all()

    for item in items:
        deadline = item.assigned_at + timedelta(hours=item.battle.quest.work_time)

        if deadline < timezone.now():
            pvps = [i for i in item.battle.pvp_assignments.all()]

            for a in pvps:
                if a.deadline < timezone.now():
                    item.self_fail()

            if item.quest.penalty:
                logger.info(f"Granting penalty to {item.user.username} cause of failed quest {item.quest.title}")
            logger.info(f"Assignment {item.id}-{item.user.username}-{item.quest.slug} failed")
