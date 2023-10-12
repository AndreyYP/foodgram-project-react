import django_filters
from django.db.models import Q
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
            or_conditions = Q()
            for tag in tags:
                or_conditions |= Q(tags__slug=tag)
            queryset = queryset.filter(or_conditions)

        return queryset

    def get_author(self, queryset, name, value):
        author_id = self.request.query_params.get('author')
        queryset = Recipe.objects.all()
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        else:
            return queryset

        return queryset

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(favorite__user=user)
            else:
                return queryset
        elif value == '1':
            raise NotAuthenticated()

        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(shopping_cart__user=user)
            else:
                return queryset
        elif value == '1':
            raise NotAuthenticated()

        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart', 'author')
