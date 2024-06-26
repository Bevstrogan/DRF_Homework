from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "lesson_name",
        "lesson_description",
        "course",
    )
    search_fields = ("name", "course")
