from django.shortcuts import render
from django.views.generic import DetailView

from battlecode.pagedata import PageData
from peer_review.models import Review


current_page = "review"


def review_list(request):
    pd = PageData(
        title="Ревью",
        description="Просмотр ревью по квестам.",
        curr_page=current_page,
    )

    reviews = Review.objects.all()

    return render(
        request,
        "review_list.html",
        context={
            "pd": pd,
            "reviews": reviews,
        },
    )


class ReviewDetailView(DetailView):
    model = Review
    template_name = "review_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Ревью",
            description="Просмотр ревью по квесту.",
            curr_page=current_page,
        )
        return context
