from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredients,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User
from .filters import IngredientsFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CreateRecipeSerializer,
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    ShowSubscriptionsSerializer,
    SubscriptionSerializer,
    TagSerializer,
)
from .utils import post_shortcut, delete_shortcut


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = None
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny, ]
    filter_backends = [IngredientsFilter, ]
    serializer_class = IngredientSerializer
    pagination_class = None
    search_filter = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'author': id
        }
        serializer = SubscriptionSerializer(
            data=data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if Subscription.objects.filter(
           user=request.user, author=author).exists():
            subscribed = get_object_or_404(
                Subscription, user=request.user, author=author
            )
            subscribed.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShowSubscriptionsViewSet(ListAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(author__user=user)
        page = self.paginate_queryset(queryset)
        serializer = ShowSubscriptionsSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class FavoriteView(APIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        return post_shortcut(self, request, id,
                             Favorite, FavoriteSerializer)

    def delete(self, request, id):
        return delete_shortcut(self, request, id, Favorite)


class CartViewSet(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        return post_shortcut(self, request, id,
                             ShoppingCart, ShoppingCartSerializer)

    def delete(self, request, id):
        return delete_shortcut(self, request, id, ShoppingCart)


@api_view(['GET'])
def download_cart(request):
    ingredients = RecipeIngredients.objects.filter(
        recipe__shopping_cart__user=request.user).values(
        'ingredient__name', 'ingredient__measurement_unit').annotate(
        amount_in_cart=Sum('amount')
    )
    ingredient_list = "Ваш список покупок:"
    for number, ingr in enumerate(ingredients):
        ingredient_list += (
            f"\n{ingr['ingredient__name']} - "
            f"{ingr['amount_in_cart']} {ingr['ingredient__measurement_unit']}"
        )
        if number < ingredients.count() - 1:
            ingredient_list += ', '
    response = HttpResponse(ingredient_list,
                            'Content-Type: application/pdf')
    file = 'shopping_list'
    response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
    return response
