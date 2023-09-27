from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe


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
        unique=True,
        max_length=254,
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
        help_text=('Укажите свое имя'),
        blank=True
    )
    last_name = models.CharField(
        verbose_name=('Фамилия'),
        max_length=150,
        help_text=('Укажите свою фамилию'),
        blank=True
    )
    password = models.CharField(
        verbose_name=('Пароль'),
        max_length=150,
        help_text=('Введите пароль'),
    )
    shopping_cart = models.ManyToManyField(Recipe, blank=True, related_name='carts')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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


class UserFollow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='followed',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        if self.user == self.author:
            raise ValidationError("Невозможно подписаться на самого себя")
        super().save()

    def __str__(self):
        return f'Автор: {self.author}, подписчик: {self.user}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')
