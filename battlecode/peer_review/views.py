from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

from battlecode.quest_settings import break_delta
from battlecode.pagedata import PageData
from battlecode.review_settings import REVIEW_COUNT

from user.models import Profile

from peer_review.models import Assignment, Review, ReviewChecklistAnswer
from peer_review.model_utils import calculate_review_pts


curr_page = "review"


def review_checklist(request: HttpRequest, slug: str, username: str):
    with transaction.atomic():
        assignment = get_object_or_404(
            Assignment.objects.select_for_update(),
            user__username=username,
            quest__slug=slug,
            status="completed",
        )

        if not Assignment.objects.filter(
            Q(status="success") | Q(status="failed") | Q(status="completed"),
            user=request.user,
            quest=assignment.quest,
            completed_at__gte=break_delta(),
        ).exists():
            return redirect("quest_reviews", slug=assignment.quest.slug)

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
            )

            completed_count = 0
            for item in checklist_items:
                work = bool(request.POST.get(f"task_{item.slug}"))
                if work:
                    completed_count += 1
                ReviewChecklistAnswer.objects.create(
                    review=review,
                    checklist_item=item,
                    work=work,
                )

            review.completed_tasks = completed_count
            review.give_pts = calculate_review_pts(
                len(checklist_items),
                completed_count,
                assignment.quest.pts,
                rating,
            )
            review.save()

            if assignment.reviews == REVIEW_COUNT:
                give_pts = assignment.reviews_avg_pts
                if give_pts > 0:
                    assignment.status = "success"
                else:
                    assignment.status = "failed"
                    give_pts = assignment.quest.penalty * -1

                profile = Profile.objects.get(user=assignment.user)

                profile.pts += give_pts
                if profile.pts < 0:
                    profile.pts = 0

                assignment.given_pts = give_pts

                profile.save()
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
