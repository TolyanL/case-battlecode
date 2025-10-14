from django.contrib import admin
from badges.models import Badge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description", "color")
    list_filter = ("slug",)
    search_fields = ("name", "slug")

    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    filter_horizontal = ("rel_quests",)
