from django.contrib import admin

from .models import Ingredient, Recipe, Cart, Tag, Favorite


EMPTY_MSG = 'пусто'

class IngredientsInRow(admin.TubularInline):
    model = Recipe.ingredients.through


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measuring']
    search_fields = ['name']
    empty_value_display = EMPTY_MSG


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'favorites']
    search_fields = ['name', 'author__username']
    list_filter = ['tags']
    empty_value_display = EMPTY_MSG
    inlines = (
        IngredientsInRow,
    )

    def favorites(self, obj):
        if Favorite.objects.filter(recipe=obj).exists():
            return Favorite.objects.filter(recipe=obj).count()
        return 0
    

@admin.register(Cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']
    search_fields = ['user__username', 'user__email']
    empty_value_display = EMPTY_MSG


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']
    search_fields = ['name', 'slug']
    empty_value_display = EMPTY_MSG


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']
    search_fields = ['user__username', 'user__email']
    empty_value_display = EMPTY_MSG