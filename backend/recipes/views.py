from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Recipe, Tag, Ingredient
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if 'ingredients' not in request.data or not request.data['ingredients']:
                return Response({'ingredients': ['Поле является обязательным']}, status=status.HTTP_400_BAD_REQUEST)

            self.perform_create(serializer)
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


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

