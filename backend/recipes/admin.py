from django.contrib import admin
from django.db.models import Count

from recipes.models import Recipe, Ingredient, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time', 'favorited_count')
    list_filter = ('author', 'tags__name', 'name')
    search_fields = ('name', 'author__username')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            favorited_count=Count('favorite'))

    def favorited_count(self, obj):
        return obj.favorited_count
    favorited_count.short_description = 'Favorites Count'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
