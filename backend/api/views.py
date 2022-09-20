from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from recipes.models import User

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import *
from recipes.models import *


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    paginator = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    paginator = None


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

