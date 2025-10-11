from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

from battlecode.pagedata import PageData
from quests.models import Assignment

from battlecode.review_settings import REVIEW_COUNT

from peer_review.models import Review, ReviewChecklistAnswer
from peer_review.model_utils import calculate_pts


curr_page = "review"


def review_checklist(request: HttpRequest, slug: str, username: str):
    assignment = get_object_or_404(
        Assignment,
        user__username=username,
        quest__slug=slug,
        status="completed",
    )

    if Review.objects.filter(assignment=assignment, user=request.user).exists():
        return redirect("quest_reviews", slug=assignment.quest.slug)
    if assignment.reviews >= REVIEW_COUNT:
        return redirect("quest_reviews", slug=assignment.quest.slug)

    checklist_items = assignment.quest.checklist.checklist_items.all()

    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        comment = request.POST.get("comment", "").strip()

        review = Review.objects.create(
            assignment=assignment,
            user=request.user,
            grade=rating,
            comment=comment,
            completed_tasks=0,
        )

        completed_count = 0
        for item in checklist_items:
            work = False
            if request.POST.get(f"task_{item.slug}", ""):
                work = True
                completed_count += 1

            ReviewChecklistAnswer.objects.create(
                review=review,
                checklist_item=item,
                work=work,
            )

        review.completed_tasks = completed_count
        review.give_pts = calculate_pts(len(checklist_items), completed_count, assignment.quest.pts, rating)
        review.save()

        assignment.review += 1
        assignment.save()

        return redirect("quest_reviews", slug=assignment.quest.slug)

    context = {
        "pd": PageData(
            title=f"Оценка: {assignment.quest.title}",
            description="Проверьте работу участника по чек-листу.",
            curr_page=curr_page,
        ),
        "item": assignment,
        "checklist": checklist_items,
    }
    return render(request, "review_checklist.html", context)
