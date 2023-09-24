from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователя."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_LEVELS = ((USER, "User"), (MODERATOR, "Moderator"), (ADMIN, "Admin"))

    role = models.CharField(
        verbose_name="Роль",
        max_length=32,
        choices=USER_LEVELS,
        default=USER
    )
    email = models.EmailField(
        verbose_name="Почта",
        blank=True,
        unique=True,
        max_length=150,
        error_messages={
            'unique': ('Email уже используется'),
        },
        help_text=('Укажите свой email'),
    )
    username = models.CharField(
        verbose_name=('Логин'),
        max_length=150,
        unique=True,
        help_text=('Укажите свой логин'),
        error_messages={
            "unique": ("Логин уже используется"),
        },
    )
    first_name = models.CharField(
        verbose_name=('Имя'),
        max_length=150,
        blank=True,
        help_text=('Укажите свое имя'),
    )
    last_name = models.CharField(
        verbose_name=('Фамилия'),
        max_length=150,
        blank=True,
        help_text=('Укажите свою фамилию'),
    )
    password = models.CharField(
        verbose_name=('Пароль'),
        max_length=150,
        help_text=('Введите пароль'),
    )
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["first_name", 'password']

    @property
    def is_administrator(self):
        return self.role == User.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_user(self):
        return self.role == User.USER

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
