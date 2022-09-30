from django.db.models import Q
from django_filters import rest_framework as filters

from .models import *


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')
    #name = filters.CharFilter(lookup_expr=(Q('istartswith') | Q('icontains')))
    #name = filters.AllValuesFilter(queryset=Ingredient.objects.all(), lookup_expr='istartswith')
    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    #is_in_shopping_cart = filters.CharFilter(method='cart')
    is_in_shopping_cart = filters.CharFilter(method='cart')
    is_favorited = filters.CharFilter(method='favorites')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug',)
    class Meta:
        model = Recipe
        fields = ('author', )

    def cart(self, queryset, name, value):
        #print(queryset, name, value)
        queryset = queryset.filter(shopping_cart__user=self.request.user)
        #print(queryset)
        return queryset

    def favorites(self, queryset, name, value):
        queryset = queryset.filter(favorite__user=self.request.user)
        return queryset
