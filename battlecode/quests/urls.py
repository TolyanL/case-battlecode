from django.urls import path

from .views import quests_all, quests_check, QuestDetailView
from .requests import accept_quest, complete_quest


urlpatterns = [
    path("", quests_all, name="quests_all"),
    path("check", quests_check, name="quests_check"),
    path("<str:slug>/", QuestDetailView.as_view(), name="quest_detail"),
    # requests routes
    path("accept", accept_quest, name="req_accept_quest"),
    path("complete", complete_quest, name="req_complete_quest"),
]
