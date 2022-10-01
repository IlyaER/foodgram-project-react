import io

from django.db.models import Sum
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import *
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.filters import *
from .paginators import PageLimitPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from .serializers import *
from recipes.models import *


class CustomUserViewSet(DjoserUserViewSet):
    pagination_class = PageLimitPagination
    #queryset = User.objects.all()
    max_page_size = 3

    @action(["get"], permission_classes=[IsAuthenticated], pagination_class=PageLimitPagination, detail=False)
    def subscriptions(self, request):
        user = self.request.user
        queryset = User.objects.filter(subscribed__user=request.user)
        #queryset = user.subscriptions.all()
        limit = request.query_params.get('recipes_limit')
        if limit:
            queryset = queryset[:int(limit)]
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


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
    permission_classes = (IsAdminOrReadOnly,)
    paginator = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    paginator = None
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    pagination_class = PageLimitPagination
    filterset_class = RecipeFilter
    #filter_backends = (DjangoFilterBackend,)

    # TODO Tags create: currently set read_only in serializers
    def get_serializer_class(self):
        #print(self.action)
        #if self.action == 'list': # retrieve
        #    return self.serializer_class
        if self.action == 'partial_update' or self.action == 'create':
            #print('RecipeWriteSerializer')
            return RecipeWriteSerializer
        return self.serializer_class

    #def create(self, request, *args, **kwargs):
    #    serializer = self.get_serializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    self.perform_create(serializer)
    #    headers = self.get_success_headers(serializer.data)
    #    #return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(["get",], permission_classes=[IsAuthenticated], detail=False)
    def download_shopping_cart(self, request):

        ingredients = Ingredient.objects.filter(
            recipes__shopping_cart__user=request.user
        ).values(
            'name',
            'measurement_unit'
        ).annotate(amount=Sum('recipe__amount')).order_by()
        print(ingredients)

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, bottomup=1)
        #pdf.setFont('Courier', 14)
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        pdf.setFont('DejaVuSans', 14)
        #print(pdf.getAvailableFonts())
        pdf.drawString(70, 770, "Список покупок.")
        for i, ingredient in enumerate(ingredients, 1):
            pdf.drawString(70, 770 - i*20, f"{i} {ingredient['name']} ({ingredient['measurement_unit']}): {ingredient['amount']}")
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        content = "Список покупок."
        #print("Список покупок.")
        #for i, ingredient in enumerate(ingredients, 1):
        #    print(f"{i} {ingredient['name']} ({ingredient['measurement_unit']}): {ingredient['amount']}")
        #response = HttpResponse(content, content_type='text/plain')
        #response['Content-Disposition'] = 'attachment; filename="Purchase.txt"'
        return FileResponse(buffer, as_attachment=False, filename='purchase.pdf')


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


