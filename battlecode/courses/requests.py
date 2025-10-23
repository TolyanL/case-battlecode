import json

from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required

from user.models import Profile
from peer_review.models import Assignment
from courses.models import Course


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

            p = Profile.objects.get(user=user)
            p.courses.add(course)
            p.save()

            return JsonResponse({"success": True, "message": "Course enrolled"})
        except Exception as e:
            print("err: ", e)
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
                    a.status = "failed"
                    a.save()
                    p.pts -= a.quest.penalty * -1

            if p.pts < 0:
                p.pts = 0

            p.save()

            return JsonResponse({"success": True, "message": "Course unenrolled"})
        except Exception as e:
            print("err: ", e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})
