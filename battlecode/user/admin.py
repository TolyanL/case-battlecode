from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "pts", "rank", "rank_as_str", "total_worktime", "placement", "updated_at", "created_at")
    list_filter = ("pts", "updated_at", "created_at")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    ordering = ["-pts"]
    date_hierarchy = "created_at"
    filter_horizontal = ("badges", "courses")
    readonly_fields = ("total_worktime", "placement", "updated_at", "created_at")

