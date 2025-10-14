from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "rank", "pts")
    list_filter = ("rank",)
    search_fields = ("user__username",)

    ordering = ["-user__username"]
    date_hierarchy = "created_at"

    filter_horizontal = ("badges",)
