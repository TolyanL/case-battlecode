from django.urls import path

from .views import all_quests

urlpatterns = [
    path("", all_quests, name="quests_all"),
]
