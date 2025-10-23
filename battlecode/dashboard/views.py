# battlecode/dashboard/views.py
from django.shortcuts import render
from django.db.models import Q
from battlecode.pagedata import PageData
from user.models import Profile
from quests.models import Quest
from peer_review.models import Assignment
from courses.models import Course
from battlecode.quest_settings import break_delta

current_page = "dashboard"

def dashboard(request):
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect("login")

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    # PTS и ранг
    pts = profile.pts if profile else 0
    rank = profile.get_rank_display() if profile else "—"
    placement = profile.placement if profile else "—"

    # Квесты: в работе, на проверке
    assignments = Assignment.objects.filter(user=request.user)
    in_progress = assignments.filter(status="active").select_related("quest")[:3]
    on_review = assignments.filter(status="completed").select_related("quest")[:3]

    # Последние завершённые (успешно/провал)
    completed_recent = assignments.filter(
        Q(status="success") | Q(status="failed")
    ).select_related("quest").order_by("-completed_at")[:5]

    # Прогресс по курсам
    enrolled_courses = Course.objects.filter(enrolled_profiles__user=request.user)
    course_progress = []
    for course in enrolled_courses:
        total = course.quests.count()
        done = Assignment.objects.filter(
            user=request.user,
            quest__in=course.quests.all(),
            status__in=["success", "failed"]
        ).count()
        course_progress.append({
            "course": course,
            "total": total,
            "done": done,
            "percent": int(done / total * 100) if total > 0 else 0
        })

    pd = PageData(
        title="Dashboard",
        description="Ваш персональный центр активности.",
        curr_page=current_page,
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