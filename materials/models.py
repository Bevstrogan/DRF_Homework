from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/course_preview",
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Владелец курса')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    lesson_name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    lesson_description = models.TextField(
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        null=True,
        blank=True,
    )
    lesson_preview = models.ImageField(
        upload_to="materials/lesson_preview",
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
        blank=True,
        null=True,
    )
    lesson_url = models.CharField(
        max_length=300,
        verbose_name="Ссылка на видео урока",
        help_text="Введите ссылку на видео урока",
        blank=True,
        null=True,
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", null=True, blank=True
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Владелец урока')
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
