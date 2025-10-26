from celery import shared_task

from courses.models import Course
from peer_review.models import CourseProgress


@shared_task()
def check_finished_courses() -> None:
    courses = Course.objects.filter(active=True).all()

    for c in courses:
        total_quests = c.quests.count()
        if total_quests == 0:
            continue

        enrolled_users = c.enrolled_profiles.select_related("user").values_list("user", flat=True)

        for user_id in enrolled_users:
            progress = CourseProgress.objects.filter(user__id=user_id, course=c, status="active").first()

            if progress and progress.completed_quests_count == total_quests:
                progress.complete()
