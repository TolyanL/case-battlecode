from django.urls import path

from .views import review_checklist


urlpatterns = [
    path("<str:slug>/<str:username>", review_checklist, name="review_detail"),
]
