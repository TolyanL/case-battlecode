from celery import shared_task
from django.db.models import Q
from django.utils import timezone

from battlecode.quest_settings import break_delta

from courses.models import Course
from peer_review.models import Assignment, CourseProgress


@shared_task()
def check_finished_courses() -> None:
    active_courses = Course.objects.filter(active=True).prefetch_related("quests")

    for course in active_courses:
        quest_ids = list(course.quests.values_list("id", flat=True))
        total_quests = len(quest_ids)

        if total_quests == 0:
            continue

        enrolled_users = course.enrolled_profiles.select_related("user").values_list("user", flat=True)

        for user_id in enrolled_users:
            progress, created = CourseProgress.objects.get_or_create(user_id=user_id, course=course)
            if progress.status in ["success", "failed"]:
                continue

            completed_quest_ids = (
                Assignment.objects.filter(
                    user_id=user_id,
                    quest_id__in=quest_ids,
                    completed_at__gte=break_delta(),
                )
                .filter(
                    Q(status="active") | Q(status="failed"),
                )
                .values_list("quest_id", flat=True)
                .distinct()
            )

            if len(completed_quest_ids) == total_quests:
                progress.status = "success"
                progress.completed_at = timezone.now()
                progress.save()

