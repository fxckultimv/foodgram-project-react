from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CartViewSet,
    FavoriteView,
    IngredientViewSet,
    RecipeViewSet,
    ShowSubscriptionsViewSet,
    SubscribeView,
    TagViewSet,
    download_cart,
)


app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_cart,
        name='download_shopping_cart'
    ),
    path(
        'recipes/<int:id>/favorite/',
        FavoriteView.as_view(),
        name='favorite'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        CartViewSet.as_view(),
        name='shopping_cart'
    ),
    path(
        'users/subscriptions/',
        ShowSubscriptionsViewSet.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),

    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
