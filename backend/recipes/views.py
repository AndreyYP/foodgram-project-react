from django.db.models import Q
from rest_framework import status, viewsets, filters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse

from api.paginators import LimitPagination
from .models import Recipe, Tag, Ingredient
from .serializers import (RecipeSerializer, TagSerializer,
                          IngredientSerializer, FavoriteSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitPagination

    def get_queryset(self):
        queryset = Recipe.objects.all()
        tag_slugs = self.request.query_params.getlist('tags')
        if tag_slugs:
            tag_filter = Q()
            for slug in tag_slugs:
                tag_filter |= Q(tags__slug=slug)
            queryset = queryset.filter(tag_filter)
        is_favorited_param = self.request.query_params.get(
            'is_favorited', None)
        if is_favorited_param == '1':
            favorited_recipe_ids = self.request.user.favorites.values_list(
                'id', flat=True)
            queryset = queryset.filter(id__in=favorited_recipe_ids)

        return queryset.distinct()

    """Favorites"""
    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def toggle_favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        tag_names = request.query_params.getlist('tags', [])
        tags = Tag.objects.filter(name__in=tag_names)
        if tag_names:
            tags = Tag.objects.filter(name__in=tag_names)
            favorite_recipes = user.favorites.filter(tags__in=tags)
        else:
            favorite_recipes = user.favorites.all()
        if request.method == 'POST':
            if favorite_recipes.filter(pk=recipe.pk).exists():
                return Response({'detail': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.favorites.add(recipe)
            recipe.tags.add(*tags)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if favorite_recipes.filter(pk=recipe.pk).exists():
                user.favorites.remove(recipe)
                return Response({'detail': 'Рецепт удален из избранного'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'detail': 'Рецепт отсутствует в избранном'},
                    status=status.HTTP_400_BAD_REQUEST)
    """Shopping cart"""
    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.shopping_cart.filter(pk=recipe.pk).exists():
                return Response({'detail': 'Рецепт уже в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.shopping_cart.add(recipe)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if user.shopping_cart.filter(pk=recipe.pk).exists():
                user.shopping_cart.remove(recipe)
                return Response({'detail': 'Рецепт удален из корзины'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'detail': 'Рецепт отсутствует в корзине, нечего удалять'},
                    status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'detail': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED)

        shopping_cart = user.shopping_cart.all()
        shopping_cart_data = "Shopping Cart List:\n"

        for recipe in shopping_cart:
            shopping_cart_data += f"Рецепт: {recipe.name}\n"
            for recipe_ingredient in recipe.recipeingredient_set.all():
                ingredient = recipe_ingredient.ingredient
                amount = recipe_ingredient.amount
                shopping_cart_data += (f"- {ingredient.name}:"
                                       f" {amount}"
                                       f" {ingredient.measurement_unit}\n")

        response = HttpResponse(shopping_cart_data,
                                content_type='text/plain')
        response['Content-Disposition'] = ('attachment;'
                                           ' filename="shopping_cart.txt"')
        return response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('name')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
