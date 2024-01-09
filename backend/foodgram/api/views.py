from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientsFilter, RecipeFilter
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, CreateRecipeSerializer, SubscriptionSerializer, FavoriteSerializer
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredients, RecipeTag, Favorite
from .permissions import IsAdminOrReadOnly
from .pagination import CustomPagination

from users.models import User, Subscription


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
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
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
    

class FavoriteView(APIView):
    
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]
    
    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        if not Favorite.objects.filter(
           user=request.user, recipe__id=id).exists():
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
