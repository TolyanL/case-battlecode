from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("auth/", include("user_auth.urls")),
    path("quests/", include("quests.urls")),
    path("users/", include("user.urls")),
    path("review/", include("peer_review.urls")),
    path("courses/", include("courses.urls")),
    path("calendar/", include("calendar_.urls")),
    path("", include("index.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
