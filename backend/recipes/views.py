from collections import defaultdict

from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse

from api.paginators import LimitPagination
from .filters import RecipeFilters
from .models import (Recipe, Tag, Ingredient,
                     Favorite, ShoppingCart, RecipeIngredient)
from .serializers import (RecipeSerializer, TagSerializer,
                          IngredientSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilters
    serializer_class = RecipeSerializer
    pagination_class = LimitPagination

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite_recipe(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe)
            if created:
                return Response({'detail': 'Рецепт добавлен в избранное'},
                                status=status.HTTP_201_CREATED)
            return Response({'detail': 'Рецепт уже в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            favorite = Favorite.objects.get(user=user, recipe=recipe)
            favorite.delete()
            return Response({'detail': 'Рецепт удален из избранного'},
                            status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({'detail': 'Рецепта нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def manage_shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'POST':
            if user.shopping_cart.filter(recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        try:
            cart_item = ShoppingCart.objects.get(user=user, recipe=recipe)
            cart_item.delete()
            return Response({'detail': 'Рецепт удален из корзины'},
                            status=status.HTTP_204_NO_CONTENT)
        except ShoppingCart.DoesNotExist:
            return Response({'detail': 'Рецепт отсутствует в корзине'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'detail': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        shopping_cart_items = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'recipe__name',
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(
            total_quantity=Sum('amount')
        ).order_by('recipe__name', 'ingredient__name')

        response_data = "Список покупок:\n"
        ingredient_totals = defaultdict(int)
        current_recipe = None

        for item in shopping_cart_items:
            recipe_name = item['recipe__name']
            ingredient_name = item['ingredient__name']
            measurement_unit = item['ingredient__measurement_unit']
            total_quantity = item['total_quantity']

            if current_recipe != recipe_name:
                current_recipe = recipe_name
                response_data += f"\nРецепт: {recipe_name}"

            ingredient_totals[(ingredient_name,
                               measurement_unit)] += total_quantity
        response_data += "\nОбщее количество ингредиентов для всех рецептов:\n"
        for (ingredient_name,
             measurement_unit), total_quantity in ingredient_totals.items():
            response_data += (f"{ingredient_name}:"
                              f" {total_quantity}"
                              f" {measurement_unit}\n")

        response = HttpResponse(response_data, content_type='text/plain')
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
