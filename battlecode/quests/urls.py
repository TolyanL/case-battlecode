from django.urls import path

from .views import quests_all, quests_check

urlpatterns = [
    path("", quests_all, name="quests_all"),
    path("check", quests_check, name="quests_check"),
]
