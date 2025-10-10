from django.urls import path

from .views import quests_all, QuestDetailView, QuestWorkView, quest_reviews
from .requests import accept_quest, give_up_quest, complete_quest


urlpatterns = [
    path("", quests_all, name="quests_all"),
    path("details/<str:slug>", QuestDetailView.as_view(), name="quest_detail"),
    path("work/<str:slug>", QuestWorkView.as_view(), name="quest_work"),
    path("reviews/<str:slug>", quest_reviews, name="quest_reviews"),
    # path("review/<str:slug>/<str:username>", quest_checklist, name="quest_review"),
    # requests routes
    path("accept", accept_quest, name="req_accept_quest"),
    path("give-up", give_up_quest, name="req_give_up"),
    path("complete", complete_quest, name="req_complete_quest"),
]
