import base64

from rest_framework import serializers
from django.core.files.base import ContentFile

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient
from users.serializers import UsersSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    measurement_unit = serializers.CharField(required=False)


class RecipeSerializer(serializers.ModelSerializer):
    # autoadd author field for current user
    #author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    author = UsersSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return int(user.favorites.filter(pk=obj.pk).exists())
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return int(user.shopping_cart.filter(pk=obj.pk).exists())
        return False

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
            'cooking_time',
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
