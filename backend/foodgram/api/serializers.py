from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField


from users.models import Subscription, User
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredients, Favorite, Cart, RecipeTag


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()
    

class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра модели Рецепт. """

    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_ingredients(self, obj):
        ingredients = RecipeIngredients.objects.filter(recipe=obj)
        
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        
        return Favorite.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        
        return Cart.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()



class RecipeIngredientSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredients
        fields = ['id', 'name', 'amount', 'measurement_unit']


class AddIngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ['id', 'amount']


class CreateRecipeSerializer(serializers.ModelSerializer):

    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]

    def validation(self, data):
        ingredients = self.initial_data.get('ingredients')
        list = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            if int(amount) < 1:
                raise serializers.ValidationError({
                   'amount': 'Количество не может быть нулевым.'
                })
            if ingredient['id'] in list:
                raise serializers.ValidationError({
                   'ingredient': 'Этот ингредиент уже есть.'
                })
            list.append(ingredient['id'])
        return data

    def create_ingredient(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredients.objects.create(
                ingredient=ingredient, recipe=recipe, amount=i['amount']
            )

    def create_tag(self, tags, recipe):
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_ingredient(ingredients, recipe)
        self.create_tag(tags, recipe)
        
        return recipe

    def update(self, instance, validated_data):

        RecipeTag.objects.filter(recipe=instance).delete()
        RecipeIngredients.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredient(ingredients, instance)
        self.create_tag(tags, instance)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')

        if validated_data.get('image'):
            instance.image = validated_data.pop('image')

        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        
        return instance

    def representation(self, instance):
        
        return RecipeSerializer(instance, context={
            'request': self.context.get('request')}).data


class ShowFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']

    def representation(self, instance):
        return ShowFavoriteSerializer(instance.recipe, context={
            'request': self.context.get('request')}).data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['user', 'recipe']

    def representation(self, instance):
        return ShowFavoriteSerializer(instance.recipe, context={
            'request': self.context.get('request')}).data
    

class ShowSubscriptionsSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed',
            'recipes', 'recipes_count']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj).exists()
    
    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        
        recipes = Recipe.objects.filter(author=obj)
        limit = request.query_params.get('recipes_limit')
        
        if limit:
            recipes = recipes[:int(limit)]

        return ShowFavoriteSerializer(
            recipes, many=True, context={'request': request}).data
    
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
    

    class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['user', 'author']
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author'],
            )
        ]

    def representation(self, instance):
        return ShowSubscriptionsSerializer(instance.author, context={
            'request': self.context.get('request')}).data
