from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    search_fields = ['name']
    empty_value_display = 'пусто'


class IngredientsInRow(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'favorites']
    search_fields = ['name', 'author__username']
    list_filter = ['tags']
    empty_value_display = 'пусто'
    inlines = (
        IngredientsInRow,
    )

    def favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']
    search_fields = ['user__username', 'user__email']
    empty_value_display = 'пусто'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']
    search_fields = ['name', 'slug']
    empty_value_display = 'пусто'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']
    search_fields = ['user__username', 'user__email']
    empty_value_display = 'пусто'
