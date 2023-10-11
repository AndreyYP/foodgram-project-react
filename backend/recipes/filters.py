import django_filters
from django.db.models import Q
from rest_framework import filters

from recipes.models import Recipe


class MultipleTagsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.getlist('tags')
        if tags:
            filter_conditions = Q()
            for tag in tags:
                filter_conditions |= Q(tags__slug=tag)
            return queryset.filter(filter_conditions)
        return queryset


class RecipeFilters(django_filters.FilterSet):
    tags = MultipleTagsFilterBackend()
    is_favorited = django_filters.CharFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.CharFilter(
        method='get_is_in_shopping_cart')

    def filter_tags(self, queryset, name, value):
        if value:
            tags = value.split(',')
            return queryset.filter(tags__slug__in=tags)
        return queryset

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(favorite__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart', 'author')
