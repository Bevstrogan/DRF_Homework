from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите ваш телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите ваш текст",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар профиля",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [("cash", "Наличные"), ("card", "Перевод")]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payments_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Дата оплаты"
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплата курса",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплата урока",
        blank=True,
        null=True,
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=15,
        default="cash",
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
    )

    def str(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payments_date"]
