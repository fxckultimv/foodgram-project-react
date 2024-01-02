from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()

class Tag(models.Model):

    name = models.CharField('Название тэга', unique=True, max_length=200)
    color = models.CharField('Цвет', uniqe=True, max_length=7)
    slug = models.SlugField('Slug', unique=True, max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = ['Тэг']
        verbose_name_plural = ['Тэги']

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):

    name = models.CharField('Название ингредиента', max_length=200)
    measuring = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [UniqueConstraint(fields=['name', 'measuring'], name='ingredient_name_unit_unique')]


class Recipe(models.Model):

    tags = models.ManyToManyField