# case-battlecode/battlecode/quests/admin.py
from django.contrib import admin
from .models import Quest, QuestDetail, Language, Skill, Assignment, QuestReviewChecklist, ChecklistItem


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "pts", "active")
    list_filter = ("difficulty", "active", "skills")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("skills",)  # Удобный виджет для ManyToMany


# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ("title", "difficulty", "base_pts", "active", "created_at")
#     list_filter = ("difficulty", "active", "skills")
#     search_fields = ("title", "description")
#     prepopulated_fields = {"slug": ("title",)}
#     # --- ИЗМЕНЕНО: Добавлено поле 'quests' в редактирование ---
#     # filter_horizontal = ('skills',) # Убираем 'quests' из-за потенциальной ошибки InvalidCursorName
#     # raw_id_fields = ('quests',) # Альтернатива: показать ID
#     # fields = ('title', 'description', 'slug', 'skills', 'base_pts', 'difficulty', 'quests', 'active') # Порядок полей
#     # --- /ИЗМЕНЕНО ---
#     fields = (
#         "title",
#         "description",
#         "slug",
#         "skills",
#         "base_pts",
#         "difficulty",
#         "quests",
#         "active",
#     )  # Добавили 'quests' в редактирование
#     filter_horizontal = ("skills",)  # Только для 'skills' из-за InvalidCursorName


@admin.register(QuestDetail)
class QuestDetailAdmin(admin.ModelAdmin):
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


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "quest", "status", "assigned_at")
    list_filter = ("status", "assigned_at")

    ordering = ["-assigned_at"]
    date_hierarchy = "assigned_at"


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1


@admin.register(QuestReviewChecklist)
class QuestReviewAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]
    list_display = ("created_at",)
