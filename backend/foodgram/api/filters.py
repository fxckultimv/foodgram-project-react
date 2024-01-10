from django_filters import rest_framework as filter
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

class RecipeFilter(filter.FilterSet):
    author = filter.CharFilter()
    tags = filter.ModelMultupleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug'
    )
    is_favorited = filter.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = filter.BooleandFilter(
        method='get_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'get_is_in_shopping_cart']

class IngredientsFilter(SearchFilter):
    search_param = 'name'
