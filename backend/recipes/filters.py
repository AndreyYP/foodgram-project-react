import django_filters
from rest_framework.exceptions import NotAuthenticated

from recipes.models import Recipe


class RecipeFilters(django_filters.FilterSet):
    is_favorited = django_filters.CharFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.CharFilter(
        method='get_is_in_shopping_cart')
    author = django_filters.CharFilter(method='get_author')
    tags = django_filters.CharFilter(method='filter_tags')

    def filter_tags(self, queryset, name, value):
        if value:
            tags = self.request.GET.getlist('tags')
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        return queryset

    def get_author(self, queryset, name, value):
        author_id = self.request.query_params.get('author')
        queryset = Recipe.objects.all()
        if author_id:
            queryset = queryset.filter(author__id=author_id)

        return queryset

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(favorite__user=user)
            else:
                return queryset
        elif not user.is_authenticated:
            if value == '1':
                raise NotAuthenticated()
            else:
                return queryset

        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(shopping_cart__user=user)
            else:
                return queryset
        elif not user.is_authenticated:
            if value == '1':
                raise NotAuthenticated()
            else:
                return queryset

        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart', 'author')
