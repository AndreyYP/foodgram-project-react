from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse

from .models import Recipe, Tag, Ingredient, RecipeIngredient
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        tag_ids = self.request.query_params.getlist('tags')
        if tag_ids:
            tags = get_object_or_404(Tag, id__in=tag_ids)
            queryset = queryset.filter(tags__in=tags)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            ingredients_data = serializer.initial_data.get('ingredients')

            if not ingredients_data:
                return Response({'ingredients': ['Поле является обязательным']}, status=status.HTTP_400_BAD_REQUEST)

            recipe = serializer.save(author=self.request.user)

            for ingredient_data in ingredients_data:
                ingredient = Ingredient.objects.get(pk=ingredient_data['id'])
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=ingredient_data['amount']
                )
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.author != user:
            raise PermissionDenied("Вы не являетесь автором рецепта")

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    """Favorites"""
    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def toggle_favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        tag_ids = request.query_params.getlist('tags')
        if tag_ids:
            tags = get_object_or_404(Tag, id__in=tag_ids)
            favorite_recipes = user.favorites.filter(tags__in=tags)
        else:
            favorite_recipes = user.favorites.all()
        if request.method == 'POST':
            if favorite_recipes.filter(pk=recipe.pk).exists():
                return Response({'detail': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.favorites.add(recipe)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if favorite_recipes.filter(pk=recipe.pk).exists():
                user.favorites.remove(recipe)
                return Response({'detail': 'Рецепт удален из избранного'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Рецепт отсутствует в избранном, нечего удалять'},
                                status=status.HTTP_400_BAD_REQUEST)
    """Shopping cart"""
    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        # POST
        if request.method == 'POST':
            if user.shopping_cart.filter(pk=recipe.pk).exists():
                return Response({'detail': 'Рецепт уже в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.shopping_cart.add(recipe)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # DELETE
        elif request.method == 'DELETE':
            if user.shopping_cart.filter(pk=recipe.pk).exists():
                user.shopping_cart.remove(recipe)
                return Response({'detail': 'Рецепт удален из корзины'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Рецепт отсутствует в корзине, нечего удалять'},
                                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        shopping_cart = user.shopping_cart.all()
        shopping_cart_data = "Shopping Cart List:\n"

        for recipe in shopping_cart:
            shopping_cart_data += f"Рецепт: {recipe.name}\n"
            for recipe_ingredient in recipe.recipeingredient_set.all():
                ingredient = recipe_ingredient.ingredient
                quantity = recipe_ingredient.quantity
                shopping_cart_data += f"- {ingredient.name}: {quantity} {ingredient.measurement_unit}\n"

        response = HttpResponse(shopping_cart_data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

