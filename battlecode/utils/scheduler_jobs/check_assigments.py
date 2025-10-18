from datetime import timedelta
from dataclasses import dataclass

from django.utils import timezone
from apscheduler.triggers.cron import CronTrigger

from user.models import Profile
from peer_review.models import Assignment

from .schefuler_job import SchedulerJob


@dataclass
class CheckAssignments(SchedulerJob):
    id: str = "check_assignments"
    trigger: any = CronTrigger(minute="*/30")

    def func(self) -> None:
        assigments = Assignment.objects.filter(status="active").all()

        for item in assigments:
            deadline = item.assigned_at + timedelta(hours=item.quest.work_time)
            print(item.quest.title, deadline)

            if deadline >= timezone.now():
                item.status = "failed"

                if penalty := item.quest.penalty:
                    profile = Profile.objects.get(user=item.user)
                    profile.pts -= penalty
                    profile.save()

                item.save()
