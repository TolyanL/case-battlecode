from django.contrib import admin
from badges.models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description", "color", "text_color", "active", "updated_at", "created_at")
    list_filter = ("active", "updated_at", "created_at")
    search_fields = ("name", "slug")
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    filter_horizontal = ("rel_quests", "rel_courses")
    readonly_fields = ("text_color", "bg_color", "updated_at", "created_at")