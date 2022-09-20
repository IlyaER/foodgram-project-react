from rest_framework import serializers

from recipes.models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    ingredients = IngredientSerializer(many=True)
    tag = TagSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = '__all__'