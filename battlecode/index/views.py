from django.shortcuts import render

from battlecode.pagedata import PageData

from quests.models import Quest
from user.models import Profile


curr_page = "index"


def index(request):
    pd = PageData(
        title="BattleCode — Learn by Doing",
        description="BattleCode — образовательная игровая платформа для программистов.",
        curr_page=curr_page,
    )

    active_quests = Quest.objects.filter(active=True)

    if request.user.is_authenticated:
        course_quests = active_quests.filter(course_quests__course__enrolled_profiles__user=request.user)
        free_quests = active_quests.filter(course_quests__isnull=True)

        featured_courses = (course_quests | free_quests)[:6]
    else:
        featured_courses = active_quests.filter(course_quests__isnull=True)[:6]

    context = {
        "pd": pd,
        "featured_quests": featured_courses,
    }

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            context["profile"] = profile
            enrolled_courses = profile.courses.all()
            context["enrolled_courses"] = enrolled_courses
        except Profile.DoesNotExist:
            pass

    return render(request, "index.html", context)
