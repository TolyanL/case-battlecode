import json

from django.utils import timezone
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required

from battlecode.course_settings import break_delta
from user.models import Profile
from peer_review.models import Assignment, CourseProgress
from courses.models import Course

from logging import getLogger


logger = getLogger(__name__)


@login_required()
def enroll_course(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)

            course_slug = data.get("slug")
            if not course_slug:
                return JsonResponse({"success": False, "message": "Empty request"})

            course = Course.objects.get(slug=course_slug)
            if not course:
                return JsonResponse({"success": False, "message": "Course not found"})

            if ct := CourseProgress.objects.filter(
                user=user,
                course=course,
            ).first():
                if ct.status in ["success", "failed"] and ct.completed_at >= break_delta():
                    print("already completed")
                    return JsonResponse({"success": False, "message": "You have already completed this course"})

            CourseProgress.objects.create(
                user=user,
                course=course,
                status="active",
            )

            p = Profile.objects.get(user=user)
            p.courses.add(course)
            p.save()

            return JsonResponse({"success": True, "message": "Course enrolled"})
        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required()
def unenroll_course(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)

            course_slug = data.get("slug")
            if not course_slug:
                return JsonResponse({"success": False, "message": "Empty request"})

            course = Course.objects.get(slug=course_slug)
            if not course:
                return JsonResponse({"success": False, "message": "Course not found"})

            p = Profile.objects.get(user=user)
            p.courses.remove(course)

            c_quests = course.quests.all()
            for q in c_quests:
                if (
                    a := Assignment.objects.filter(user=user, quest=q)
                    .filter(Q(status="active") | Q(status="completed"))
                    .first()
                ):
                    a.fail()

            CourseProgress.objects.update(
                user=user,
                course=course,
                completed_at=timezone.now(),
                status="failed",
            )

            return JsonResponse({"success": True, "message": "Course unenrolled"})
        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})
