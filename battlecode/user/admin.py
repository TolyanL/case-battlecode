from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "pts", "rank", "rank_as_str", "total_worktime", "placement", "updated_at", "created_at")
    # Убираем 'rank' из list_filter, так как это @property
    list_filter = ("pts", "updated_at", "created_at")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    ordering = ["-pts"]
    date_hierarchy = "created_at"
    filter_horizontal = ("badges", "courses")
    # Убираем 'rank' из readonly_fields, если оно не сохраняется в БД
    readonly_fields = ("pts", "rank", "rank_as_str", "total_worktime", "placement", "updated_at", "created_at")