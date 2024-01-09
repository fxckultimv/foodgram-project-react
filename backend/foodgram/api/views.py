from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .serializers import TagSerializer
from recipes.models import Tag


class TagViewSet(viewset.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = None
    setializer_class = TagSerializer


class IngredientViewSet(viewset.ReadOnlyModelViewSet):
