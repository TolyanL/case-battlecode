# quests/urls.py

from django.urls import path
from .views import (
    quests_all,
    quests_check,
    QuestDetailView,
    quest_checklist,
    quest_reviews,
)
from .requests import accept_quest

urlpatterns = [
    path("", quests_all, name="quests_all"),
    path("check", quests_check, name="quests_check"),
    path("<str:slug>/", QuestDetailView.as_view(), name="quest_detail"),
    path("<str:slug>/checklist/", quest_checklist, name="quest_checklist"),
    path("<str:slug>/reviews/", quest_reviews, name="quest_reviews"),
    # requests routes
    path("accept", accept_quest, name="req_accept_quest"),
]