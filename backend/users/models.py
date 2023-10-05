from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

MAX_LEN254 = 254
MAX_LEN150 = 150


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Почта",
        unique=True,
        max_length=MAX_LEN254,
        error_messages={
            'unique': ('Email уже используется'),
        },
        help_text=('Укажите свой email'),
    )
    username = models.CharField(
        verbose_name=('Логин'),
        max_length=MAX_LEN150,
        unique=True,
        help_text=('Укажите свой логин'),
        error_messages={
            "unique": ("Логин уже используется"),
        },
    )
    first_name = models.CharField(
        verbose_name=('Имя'),
        max_length=MAX_LEN150,
        help_text=('Укажите свое имя')
    )
    last_name = models.CharField(
        verbose_name=('Фамилия'),
        max_length=MAX_LEN150,
        help_text=('Укажите свою фамилию')
    )
    password = models.CharField(
        verbose_name=('Пароль'),
        max_length=MAX_LEN150,
        help_text=('Введите пароль'),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Пользователь"

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
        unique_together = ('user', 'author')
