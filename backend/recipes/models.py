from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(unique=True)


class Ingredients(models.Model):
    """
    Список всех возможных составных частей для блюд
    """
    name = models.CharField(max_length=64)
    measurement_unit = models.CharField(max_length=32)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=64)
    image = models.ImageField(
        upload_to='recipes/images/',
        default=None
        )
    text = models.TextField(max_length=1200)
    ingredient = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredients',
        related_name='recipe',
    )
    tag = models.ManyToManyField(
        Tag,
        through='RecipesTags'
    )
    cooking_time = models.IntegerField()


class RecipesTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=8)
    #measure = models.CharField(max_length=32)


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber'
    )
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='На кого подписан',
        related_name='subscribed'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscribed_to'],
                name='unique subscribers'
            )
        ]

