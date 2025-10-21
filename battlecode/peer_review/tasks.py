from datetime import timedelta
from celery import shared_task

from django.utils import timezone

from user.models import Profile
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
            item.status = "failed"

            if penalty := item.quest.penalty:
                profile = Profile.objects.get(user=item.user)
                profile.pts -= penalty
                profile.save()
                logger.info("Granting penalty")

            item.save()
            logger.info(f"Assignment {item.id}-{item.user.username}-{item.quest.slug} failed")
