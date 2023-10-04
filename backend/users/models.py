from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
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
        help_text=('Укажите свое имя')
    )
    last_name = models.CharField(
        verbose_name=('Фамилия'),
        max_length=150,
        help_text=('Укажите свою фамилию')
    )
    password = models.CharField(
        verbose_name=('Пароль'),
        max_length=150,
        help_text=('Введите пароль'),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
