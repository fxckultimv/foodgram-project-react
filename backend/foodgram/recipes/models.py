from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):

    name = models.CharField('Название тэга',
                            unique=True,
                            max_length=200)
    color = models.CharField('Цвет',
                             unique=True,
                             max_length=7)
    slug = models.SlugField('Slug',
                            unique=True,
                            max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = ['Тэг']
        verbose_name_plural = ['Тэги']

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField('Название ингредиента',
                            max_length=200)
    measurement_unit = models.CharField('Единицы измерения',
                                        max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [UniqueConstraint(fields=['name', 'measurement_unit'],
                                        name='ingredient_name_unit_unique')]


class Recipe(models.Model):

    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Тэги',
        related_name='tags'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Ингредиенты'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField('Изображение', upload_to='recipes/images/')
    name = models.CharField('Название рецепта', max_length=200)
    text = models.TextField('Описание для рецепта',
                            help_text='Введите описание блюда')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время готовки',
        validators=[MinValueValidator(
            1,
            message='Время готовки не может быть равно 0.'
        )]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        default=1,
        validators=(MinValueValidator(1, 'Минимум 1'),),
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'В рецепте {self.recipe.name} {self.amount} '
                f'{self.ingredient.measurement_unit} {self.ingredient.name}')


class RecipeIngredients(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(MinValueValidator(
            1, message='Мин. количество ингридиентов 1'),),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'В рецепте {self.recipe} есть ингредиент {self.ingredient}'


class RecipeTag(models.Model):

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тэг')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='recipe_tag_unique'
            )
        ]


class Favorite(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorites')

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт', related_name='favorites')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='user_favorite_unique'
                             )
        ]


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт', related_name='shopping_cart'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_cart_unique'
            )
        ]
