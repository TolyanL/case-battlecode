from django.urls import path

from .views import quests_all, quests_check, QuestDetailView, QuestWorkView
from .requests import accept_quest, give_up_quest, complete_quest


urlpatterns = [
    path("", quests_all, name="quests_all"),
    path("check", quests_check, name="quests_check"),
    path("details/<str:slug>", QuestDetailView.as_view(), name="quest_detail"),
    path("work/<str:slug>", QuestWorkView.as_view(), name="quest_work"),
    # requests routes
    path("accept", accept_quest, name="req_accept_quest"),
    path("give-up", give_up_quest, name="req_give_up"),
    path("complete", complete_quest, name="req_complete_quest"),
]
