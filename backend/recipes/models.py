from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """
    Список всех возможных составных частей для блюд
    """
    name = models.CharField(max_length=64)
    measurement_unit = models.CharField(max_length=32)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipe'
    )
    name = models.CharField(max_length=64)
    image = models.ImageField(
        upload_to='recipes/images/',
        default=None
        )
    text = models.TextField(max_length=1200)
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredients',
        related_name='recipe',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipesTags',
        related_name='recipe',
    )
    cooking_time = models.IntegerField()


class RecipesTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients_to')
    name = models.ForeignKey(Ingredients, on_delete=models.CASCADE, related_name='recipes')
    amount = models.IntegerField(blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'name'],
                name='unique ingredients'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    favorite_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite_recipe'],
                name='unique favorites'
            )
        ]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_cart')
    cart_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='shopping_cart')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'cart_recipe'],
                name='unique purchase'
            )
        ]

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

