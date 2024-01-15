from django.shortcuts import get_object_or_404 
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from users.models import Subscription



def check_subscription(self, obj):
    request = self.context.get('request')
    if request is None or request.user.is_anonymous:
        return False
    return Subscription.objects.filter(user=request.user, author=obj).exists()


def post_shortcut(self, request, id, model_obj, serializer_obj):
    data = {
        'user': request.user.id,
        'recipe': id
    }
    if not model_obj.objects.filter(
            user=request.user, recipe__id=id).exists():
        serializer = serializer_obj(
            data=data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def delete_shortcut(self, request, id, model_obj):
    recipe = get_object_or_404(Recipe, id=id)
    if model_obj.objects.filter(
       user=request.user, recipe=recipe).exists():
        model_obj.objects.filter(user=request.user, recipe=recipe).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
