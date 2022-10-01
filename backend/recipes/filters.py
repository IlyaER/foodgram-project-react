from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    is_in_shopping_cart = filters.CharFilter(method='cart')
    is_favorited = filters.CharFilter(method='favorites')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug',)

    class Meta:
        model = Recipe
        fields = ('author', )

    def cart(self, queryset, name, value):
        queryset = queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    def favorites(self, queryset, name, value):
        queryset = queryset.filter(favorite__user=self.request.user)
        return queryset
