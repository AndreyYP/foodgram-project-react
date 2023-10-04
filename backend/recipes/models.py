from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator, ValidationError
from django.db import models
from django.conf import settings

User = get_user_model()

MAX_LEN200 = 200


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField(max_length=MAX_LEN200)
    image = models.ImageField(upload_to='recipes_images/')
    text = models.TextField()
    ingredients = models.ManyToManyField('Ingredient',
                                         through='RecipeIngredient')
    tags = models.ManyToManyField('Tag')
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1)],)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)


hex_color_validator = RegexValidator(
    regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
    message='Введите правильный hex-код цвета (например, "#RRGGBB").'
)


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LEN200, unique=True)
    color = models.CharField(
        max_length=7,
        validators=[hex_color_validator]
    )

    def save(self, *args, **kwargs):
        if Tag.objects.filter(color=self.color).exclude(pk=self.pk).exists():
            raise ValidationError('Цвет должен быть уникальным для каждого тега.')
        super().save(*args, **kwargs)
    slug = models.SlugField(unique=True, max_length=MAX_LEN200)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LEN200)
    measurement_unit = models.CharField(max_length=MAX_LEN200)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],)

    def __str__(self):
        return self.name


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
