from django.urls import path

from .views import user_profile

urlpatterns = [
    path("profile/<str:username>", user_profile, name="user_profile"),
]
