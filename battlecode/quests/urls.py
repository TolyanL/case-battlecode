from django.urls import path
from .views import quests_all, quests_check, QuestDetailView

urlpatterns = [
    path("", quests_all, name="quests_all"),
    path("check", quests_check, name="quests_check"),
    path("<str:slug>/", QuestDetailView.as_view(), name="quest_detail"),
]

