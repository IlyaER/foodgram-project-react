from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from recipes.models import User

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import *
from recipes.models import *


class CustomUserViewSet(DjoserUserViewSet):
    pagination_class = PageNumberPagination

    @action(["get"], detail=False)
    def subscriptions(self, request):
        user = self.request.user
        queryset = user.subscriptions.all()
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
        #return Response(serializer.data)
        #return self.request.user.subscriber.all()

    @action(["post", "delete"], permission_classes=[IsAuthenticated], detail=True)
    def subscribe(self, request, id):
        user = self.request.user
        if request.method == 'DELETE':
            #subscribed_to = Subscribe.objects.filter(
            #    user=user,
            #    subscribed_to=id
            #)
            subscribed_to = get_object_or_404(Subscribe, user=user, subscribed_to=id)
            subscribed_to.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = SubscribeSerializer(
            context={'request': self.request},
            data={'user': user.id, 'subscribed_to': id}
        )
        #print(serializer.initial_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # при подписке переводим на страницу с подписками, но без пагинатора
            queryset = user.subscriptions.all()
            serializer = SubscriptionSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_404_NOT_FOUND)



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
    #permission_classes = (IsAuthenticated,)

    # TODO Tags create: currently set read_only in serializers
    def get_serializer_class(self):
        print(self.action)
        #if self.action == 'list': # retrieve
        #    return self.serializer_class
        if self.action == ('partial_update' or 'create'):
            return RecipeWriteSerializer
        return self.serializer_class

    #def create(self, request, *args, **kwargs):
    #    #serializer = self.get_serializer(data=request.data)
    #    serializer = RecipeWriteSerializer(data=request.data)
    #    #print(f'Initial data (viewset create method):{serializer.initial_data}')
    #    #ingredients = serializer.initial_data.pop('ingredients')
    #    serializer.is_valid(raise_exception=True)
    #    #print(serializer)
    #    self.perform_create(serializer)
    #    headers = self.get_success_headers(serializer.data)
    #    #return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        return serializer.save(author=self.request.user
            #category=category, genre=genre, description=description
        )

    @action(["post", "delete"], permission_classes=[IsAuthenticated], detail=True)
    def shopping_cart(self, request, pk):
        user = self.request.user
        if request.method == 'DELETE':
            cart_recipe = get_object_or_404(Cart, user=user, cart_recipe=pk)
            cart_recipe.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = CartSerializer(
            context={'request': self.request},
            data={'user': user.id, 'cart_recipe': pk}
        )
        #print(serializer.initial_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # TODO: при подписке переводим на страницу с рецептом
            #queryset = Recipe.objects.all()
            #serializer = ShortRecipeSerializer(queryset, source='recipe', many=True, read_only=True, context={'request': request})
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_404_NOT_FOUND)


    @action(["post", "delete"], permission_classes=[IsAuthenticated], detail=True)
    def favorite(self, request, pk):
        user = self.request.user
        if request.method == 'DELETE':
            favorite_recipe = get_object_or_404(Favorite, user=user, favorite_recipe=pk)
            favorite_recipe.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = FavoriteSerializer(
            context={'request': self.request},
            data={'user': user.id, 'favorite_recipe': pk}
        )
        #print(serializer.initial_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # TODO: при подписке переводим на страницу с рецептом
            #queryset = Recipe.objects.all()
            #serializer = ShortRecipeSerializer(queryset, source='recipe', many=True, read_only=True, context={'request': request})
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_404_NOT_FOUND)


#class SubscribeViewSet(ModelViewSet):
#    serializer_class = SubscribeSerializer
#
#    #permission_classes = (IsAuthenticated, )
#    #filter_backends = (filters.SearchFilter, )
#    search_fields = ('is_subscribed__username',)
#
#    def get_queryset(self):
#        return self.request.user.subscriber.all()
#
#    def perform_create(self, serializer):
#        serializer.save(user=self.request.user)
