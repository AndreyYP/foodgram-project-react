import base64

from rest_framework import serializers
from django.core.files.base import ContentFile

from recipes.models import Recipe, Tag, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time_minutes',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            try:
                format, imgstr = data.split(';base64,')
                ext = format.split('/')[-1]
                valid_content_types = ['image/jpeg', 'image/png']
                if format not in valid_content_types:
                    raise serializers.ValidationError('Invalid image format')
                decoded_image = base64.b64decode(imgstr)
                data = ContentFile(decoded_image, name=f'photo.{ext}')
            except Exception as e:
                raise serializers.ValidationError('Invalid Base64 format')
        return super().to_internal_value(data)
