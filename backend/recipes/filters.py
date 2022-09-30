from django_filters import rest_framework as filters

from .models import *


class RecipeFilter(filters.FilterSet):
    #'is_in_shopping_cart'
    #'is_favorited'
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug',)
    class Meta:
        model = Recipe
        fields = ('tags', )