from django.contrib import admin
from .models import Quest, Language, Skill


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "created_at")
    list_filter = ("active", "created_at")
    search_fields = ("title", "description")

    ordering = ["-created_at"]
    date_hierarchy = "created_at"


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ("slug",)
    search_fields = ("name", "slug")

    ordering = ["-created_at"]
    date_hierarchy = "created_at"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "slug")
    list_filter = ("slug",)
    search_fields = ("name", "slug")

    ordering = ["-created_at"]
    date_hierarchy = "created_at"
