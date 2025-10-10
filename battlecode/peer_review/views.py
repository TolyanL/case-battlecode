from django.http import HttpRequest
from django.shortcuts import render, redirect

from battlecode.pagedata import PageData
from quests.models import Assignment
from peer_review.models import Review


current_page = "review"


def review_checklist(request: HttpRequest, slug: str, username: str):
    item = Assignment.objects.filter(user__username=username, quest__slug=slug, status="completed").first()
    if not item:
        return redirect("quest_reviews", slug=slug)

    context = {}
    checklist_items = item.quest.checklist.checklist_items.all()

    if request.method == "POST":
        for i, _ in enumerate(checklist_items):
            value = request.POST.get(f"criteria_{i}")
            print(f"  Критерий {i}: {value}")

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        print(f"  Оценка: {rating}, Комментарий: {comment}")
        return redirect("quest_reviews", slug=item.quest.slug)

    context["pd"] = PageData(
        title=f"Оценка: {item.quest.title}",
        description="Проверьте работу участника по чек-листу.",
        curr_page=current_page,
    )

    context["item"] = item
    context["checklist"] = checklist_items

    return render(request, "review_checklist.html", context)


# TODO: Save to db:
# checklist_id
# checklist with checked items
# ^-- add to Review model
