from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


class Recipe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes_images/')
    text = models.TextField()
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')
    tags = models.ManyToManyField('Tag')
    cooking_time_minutes = models.PositiveIntegerField()
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color_code = models.CharField(max_length=7, null=True)
    slug = models.SlugField(unique=True,
                            max_length=200,
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                            )])

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    measurement_unit = models.CharField(max_length=200)
