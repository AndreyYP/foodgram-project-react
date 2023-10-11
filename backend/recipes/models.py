from django.contrib.auth import get_user_model
from django.core.validators import (RegexValidator,
                                    MinValueValidator,
                                    ValidationError)
from django.db import models

User = get_user_model()

MAX_NAME = 200
MAX_HEX = 7


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField(max_length=MAX_NAME)
    image = models.ImageField(upload_to='recipes_images/')
    text = models.TextField()
    ingredients = models.ManyToManyField('Ingredient',
                                         through='RecipeIngredient')
    tags = models.ManyToManyField('Tag')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)


hex_color_validator = RegexValidator(
    regex=r'^#([A-F0-9]{6}|[A-F0-9]{3})$',
    message='Введите правильный hex-код цвета (например, "#RRGGBB").'
            ' Либо такой hex-код уже существует.')


class Tag(models.Model):
    name = models.CharField(max_length=MAX_NAME, unique=True)
    color = models.CharField(
        max_length=MAX_HEX,
        validators=[hex_color_validator]
    )
    slug = models.SlugField(unique=True, max_length=MAX_NAME)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Tag.objects.filter(color=self.color).exclude(pk=self.pk).exists():
            raise ValidationError(
                'Цвет должен быть уникальным для каждого тега.')
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_NAME)
    measurement_unit = models.CharField(max_length=MAX_NAME)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'measurement_unit')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe',
                               on_delete=models.CASCADE,
                               related_name='recipeingredients')
    ingredient = models.ForeignKey('Ingredient',
                                   on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],)


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite'
    )

    class Meta:
        unique_together = ('user', 'recipe')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart'
    )

    class Meta:
        unique_together = ('user', 'recipe')
