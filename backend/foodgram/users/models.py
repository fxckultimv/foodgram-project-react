from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.db import models

from .validators import username_validator


class User(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=200,
                                validators=[username_validator])
    email = models.EmailField('Почта', unique=True,
                              max_length=200)
    first_name = models.CharField('Имя', blank=False,
                                  max_length=200)
    last_name = models.CharField('Фамилия', blank=False,
                                 max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username


class Subscription(models.Model):

    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='подписчик'
    )

    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='subscribe_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} оформил подписку на {self.author}'
