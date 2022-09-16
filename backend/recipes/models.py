from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    USERROLES = [
        (USER, 'User'),
        (ADMIN, 'Admin')
    ]
    access = models.CharField(
        'Доступы',
        max_length=20,
        choices=USERROLES,
        default=USER
    )

    # @property
    # def is_admin(self):
    #     return self.access == self.ADMIN

    class Meta:
        ordering = ('pk',)


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    color = models.CharField(max_length=6, unique=True)
    slug = models.SlugField(unique=True)


class Components(models.Model):
    """
    Список всех возможных составных частей для блюд
    """
    name = models.CharField(max_length=64)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=64)
    picture = models.ImageField(
        upload_to='recipes/images/',
        default=None
        )
    description = models.TextField(max_length=1000, blank=True, null=True)
    ingredient = models.ManyToManyField(
        Components,
        through='Ingredients',
        related_name='recipe',
    )
    tag = models.ManyToManyField(
        Tag,
        through='RecipesTags'
    )
    prep_time = models.IntegerField()


class RecipesTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.ForeignKey(Components, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=8)
    measure = models.CharField(max_length=32)




