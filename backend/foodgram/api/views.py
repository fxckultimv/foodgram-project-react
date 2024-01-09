from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .filters import IngredientsFilter
from .serializers import TagSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient


class TagViewSet(viewset.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = None
    setializer_class = TagSerializer


class IngredientViewSet(viewset.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny, ]
    filter_backends = [IngredientsFilter, ]
    serializer_class = IngredientsFilter
    pagination_class = None
    search_filter = ['^name', ]
