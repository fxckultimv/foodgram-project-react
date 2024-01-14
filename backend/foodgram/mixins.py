from api.serializers import ShowFavoriteSerializer
from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Recipe, ShoppingCart
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ShoppingCartFavoriteMixin(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = ShowFavoriteSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_create_queryset(self, instance):
        raise NotImplementedError

    def get_delete_queryset(self, user, instance):
        raise NotImplementedError

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance, created = self.get_create_queryset(recipe)
        if created:
            serializer = self.get_serializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance = self.get_delete_queryset(user, recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(ShoppingCartFavoriteMixin):
    def get_create_queryset(self, instance):
        return Favorite.objects.get_or_create(
            user=self.request.user,
            recipe=instance,
        )

    def get_delete_queryset(self, user, instance):
        return get_object_or_404(Favorite, user=user, recipe=instance)


class CartViewSet(ShoppingCartFavoriteMixin):
    def get_create_queryset(self, instance):
        return ShoppingCart.objects.get_or_create(
            user=self.request.user,
            recipe=instance,
        )

    def get_delete_queryset(self, user, instance):
        return get_object_or_404(ShoppingCart, user=user, recipe=instance)