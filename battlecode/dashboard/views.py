from django.db.models import Q
from django.shortcuts import render, redirect

from battlecode.pagedata import PageData

from user.models import Profile
from peer_review.models import Assignment
from courses.models import Course
from peer_review.models import CourseProgress


curr_page = "dashboard"


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile

    pts = profile.pts if profile else 0
    rank = profile.rank_as_str if profile else "—"
    placement = profile.placement if profile else "—"

    assignments = Assignment.objects.filter(user=request.user)
    in_progress = assignments.filter(status="active").select_related("quest")[:3]
    on_review = assignments.filter(status="completed").select_related("quest")[:3]

    completed_recent = (
        assignments.filter(Q(status="success") | Q(status="failed"))
        .select_related("quest")
        .order_by("-completed_at")[:5]
    )

    enrolled_courses = Course.objects.filter(enrolled_profiles__user=request.user)
    course_progress = []

    for course in enrolled_courses:
        progress_obj = CourseProgress.objects.filter(user=request.user, course=course).first()
        if not progress_obj:
            continue

        percent = progress_obj.progress_percent
        total = course.quests.count()
        done = progress_obj.completed_quests_count

        course_progress.append({"course": course, "total": total, "done": done, "percent": percent})

    pd = PageData(
        title="Dashboard",
        description="Ваш персональный центр активности.",
        curr_page=curr_page,
    )

    context = {
        "pd": pd,
        "profile": profile,
        "pts": pts,
        "rank": rank,
        "placement": placement,
        "in_progress": in_progress,
        "on_review": on_review,
        "completed_recent": completed_recent,
        "course_progress": course_progress,
    }

    return render(request, "dashboard.html", context)
