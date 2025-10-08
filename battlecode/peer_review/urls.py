from django.urls import path

from .views import review_list, ReviewDetailView


urlpatterns = [
    path("", review_list, name="review_list"),
    path("<str:slug>/", ReviewDetailView.as_view(), name="review_detail"),
]
