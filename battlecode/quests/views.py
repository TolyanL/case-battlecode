from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpRequest

from battlecode.pagedata import PageData

from quests.models import Quest, Assignment


current_page = "quests"


def quests_all(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )

    quests = Quest.objects.filter(active=True)
    accepted = Assignment.objects.filter(user=request.user, status="active").all()
    accepted_list = [item.quest.slug for item in accepted]

    return render(
        request,
        "quests_all.html",
        context={
            "pd": pd,
            "quests": quests,
            "accepted": accepted,
            "accepted_list": accepted_list,
        },
    )


class QuestDetailView(DetailView):
    model = Quest
    template_name = "quest_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Quest Detail",
            description="Details about the selected quest.",
            curr_page=current_page,
        )
        accepted = Assignment.objects.filter(user=self.request.user, status="active").all()
        context["accepted_list"] = [item.quest.slug for item in accepted]
        return context


class QuestWorkView(DetailView):
    model = Quest
    template_name = "quest_work.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Quest Detail",
            description="Details about the selected quest.",
            curr_page=current_page,
        )
        accepted = Assignment.objects.filter(user=self.request.user, status="active").all()
        context["accepted_list"] = [item.quest.slug for item in accepted]
        context["work_timer"] = timedelta(hours=self.object.work_time)

        completed = Assignment.objects.filter(user=self.request.user, status="completed").all()
        context["completed_list"] = [item.quest.slug for item in completed]

        return context


def quest_reviews(request: HttpRequest, slug: str):
    quest = get_object_or_404(Quest, slug=slug, active=True)

    context = {}
    context["pd"] = PageData(
        title=f"Проверка: {quest.title}",
        description="Список работ участников для оценки.",
        curr_page=current_page,
    )
    context["quest"] = quest
    context["items"] = Assignment.objects.filter(quest=quest, status="completed").all()

    return render(request, "quest_reviews.html", context)


def quest_checklist(request: HttpRequest, slug: str, username: str):
    quest = get_object_or_404(Quest, slug=slug, active=True)

    criteria = [
        "Отправил рабочий код",
        "Написал README.md",
        "Использовал систему контроля версий (Git)",
        "Прошёл все тесты",
        "Задокументировал архитектуру решения",
        "Соблюдал стиль кода",
        "Решение оптимально по времени/памяти",
        "Нет копипасты",
    ]

    if request.method == "POST":
        print("Форма отправлена (заглушка):")
        for i, _ in enumerate(criteria):
            value = request.POST.get(f"criteria_{i}")
            print(f"  Критерий {i}: {value}")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        print(f"  Оценка: {rating}, Комментарий: {comment}")
        success = True
    else:
        success = False

    pd = PageData(
        title=f"Оценка: {quest.title}",
        description="Проверьте работу участника по чек-листу.",
        curr_page=current_page,
    )

    return render(
        request,
        "quest_checklist.html",
        {
            "pd": pd,
            "quest": quest,
            "criteria": criteria,
            "success": success,
        },
    )
