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


class SubscribeViewSet(ModelViewSet):
    serializer_class = SubscribeSerializer

    #permission_classes = (IsAuthenticated, )
    #filter_backends = (filters.SearchFilter, )
    search_fields = ('is_subscribed__username',)

    def get_queryset(self):
        return self.request.user.subscriber.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
