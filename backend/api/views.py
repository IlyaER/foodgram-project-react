from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from recipes.models import User

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import *
from recipes.models import *


class DjoserUserViewSet(UserViewSet):

    @action(["get"], detail=False)
    def subscriptions(self, request):
        user = self.request.user
        #queryset = User.objects.filter(email=self.request.user.email)
        queryset = user.subscriptions.all()

        serializer = SubscribeSerializer(queryset, many=True, )#context={'request': request})
        return Response(serializer.data)
        #return self.request.user.subscriber.all()

    @action(["post", "delete"], detail=True)
    def subscribe(self, request, id):

        return id



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

    # TODO Tags create: currently set read_only in serializers
    #def create(self, request, *args, **kwargs):
    #    serializer = self.get_serializer(data=request.data)
    #    print(serializer.initial_data)
    #    serializer.is_valid(raise_exception=True)
    #    print(serializer)
    #    self.perform_create(serializer)
    #    headers = self.get_success_headers(serializer.data)
    #    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
    #def perform_create(self, serializer):
    #    return serializer.save(
    #        #category=category, genre=genre, description=description
    #    )

class SubscribeViewSet(ModelViewSet):
    serializer_class = SubscribeSerializer

    #permission_classes = (IsAuthenticated, )
    #filter_backends = (filters.SearchFilter, )
    search_fields = ('is_subscribed__username',)

    def get_queryset(self):
        return self.request.user.subscriber.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
