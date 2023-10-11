import django_filters
from django.db.models import Q

from recipes.models import Recipe


class TagsFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            values = value.split(',')
            return super(TagsFilter, self).filter(qs, values)
        return qs


class RecipeFilters(django_filters.FilterSet):
    tags = TagsFilter(field_name='tags__slug', method='filter_tags')
    is_favorited = django_filters.CharFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.CharFilter(
        method='get_is_in_shopping_cart')

    def filter_tags(self, queryset, name, value):
        if value:
            tags = value.split(',')
            tag_filter = Q()
            for tag in tags:
                tag_filter |= Q(tags__slug=tag)
            return queryset.filter(tag_filter)
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
