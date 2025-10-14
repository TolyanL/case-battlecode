from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
# from import_export.admin import ImportExportActionModelAdmin
# TODO: Implement

from .models import Quest, QuestDetail, Language, Skill, QuestReviewChecklist, ChecklistItem


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "pts", "active")
    list_filter = ("difficulty", "active", "skills")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("skills",)


@admin.register(QuestDetail)
class QuestDetailAdmin(SummernoteModelAdmin):
    summernote_fields = ("task",)

    list_display = ("updated_at", "created_at")
    list_filter = ("updated_at",)

    ordering = ["-updated_at"]
    date_hierarchy = "updated_at"


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


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1


@admin.register(QuestReviewChecklist)
class QuestReviewAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]
    list_display = ("created_at",)
