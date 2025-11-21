from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Quest, Language, Skill, QuestReviewChecklist, ChecklistItem

@admin.register(Quest)
class QuestAdmin(SummernoteModelAdmin):
    list_display = ("title", "difficulty", "pts", "base_pts", "penalty", "active", "updated_at", "created_at")
    list_filter = ("difficulty", "base_pts", "penalty", "active", "skills", "language")
    search_fields = ("title", "description")
    filter_horizontal = ("skills",)
    summernote_fields = ("task",)
    readonly_fields = ("pts", "updated_at", "created_at")

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "active", "updated_at", "created_at")
    list_filter = ("name", "color", "active", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "active", "updated_at", "created_at")
    list_filter = ("name", "value", "active", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 0

@admin.register(QuestReviewChecklist)
class QuestReviewAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]
    list_display = ("id", "created_at", "updated_at") # Добавил id для ясности
    readonly_fields = ("updated_at", "created_at")

# ChecklistItem не добавляю в админку отдельно, т.к. он встраивается в QuestReviewChecklist