from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "pts", "updated_at", "created_at")
    list_filter = ("user", "pts", "updated_at", "created_at")
    search_fields = ("user__username",)

    ordering = ["-user__username"]
    date_hierarchy = "created_at"

    filter_horizontal = ("badges", "courses")
