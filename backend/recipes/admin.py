from django.contrib import admin
from .models import Recipe, Ingredient, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time_minutes')
    list_filter = ('author', 'tags__name', 'name')
    search_fields = ('name', 'author__username')

    # на странице рецепта вывести общее число добавлений этого рецепта в избранное;
    #def total_favorites(self, obj):
    #    return obj.favorited_by.count()
#
    #total_favorites.short_description = 'Total Favorites'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code', 'slug')
    list_filter = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
