from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from peer_review.models import Assignment

from logging import getLogger


logger = getLogger(__name__)


@shared_task()
def check_assignments() -> None:
    assigments = Assignment.objects.filter(status="active").all()

    logger.info(f"Checking {len(assigments)} assignments")

    for item in assigments:
        deadline = item.assigned_at + timedelta(hours=item.quest.work_time)

        if deadline < timezone.now():
            item.fail()
            if item.quest.penalty:
                logger.info(f"Granting penalty to {item.user.username} cause of failed quest {item.quest.title}")
            logger.info(f"Assignment {item.id}-{item.user.username}-{item.quest.slug} failed")
