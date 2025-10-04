from django.shortcuts import render, get_object_or_404
from .models import Quest
from battlecode.pagedata import PageData

current_page = "quests"

def quests_all(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    quests = Quest.objects.filter(is_active=True)  # Только активные
    return render(request, "quests_all.html", context={
        "pd": pd,
        "quests": quests
    })

def quest_detail(request, pk):
    pd = PageData(
        title="Quest Detail",
        description="Details about the selected quest.",
        curr_page=current_page,
    )
    quest = get_object_or_404(Quest, pk=pk, is_active=True)
    return render(request, "quest_detail.html", context={
        "pd": pd,
        "quest": quest
    })

def quests_check(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "quests_check.html", context={"pd": pd})