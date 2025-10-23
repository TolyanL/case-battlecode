from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
# from import_export.admin import ImportExportActionModelAdmin
# TODO: Implement

from .models import Quest, Language, Skill, QuestReviewChecklist, ChecklistItem


@admin.register(Quest)
class QuestAdmin(SummernoteModelAdmin):
    list_display = ("title", "difficulty", "pts", "penalty", "active", "updated_at", "created_at")
    list_filter = ("difficulty", "base_pts", "penalty", "active", "skills")
    search_fields = ("title", "description")
    filter_horizontal = ("skills",)

    summernote_fields = ("task",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "active", "updated_at", "created_at")
    list_filter = ("name", "color", "created_at", "updated_at")
    search_fields = ("name",)

    ordering = ["-created_at"]
    date_hierarchy = "created_at"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "updated_at", "created_at")
    list_filter = ("name", "value", "created_at", "updated_at")
    search_fields = ("name",)

    ordering = ["-created_at"]
    date_hierarchy = "created_at"


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1


@admin.register(QuestReviewChecklist)
class QuestReviewAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]
    list_display = ("created_at",)
