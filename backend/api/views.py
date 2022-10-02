import io

from django.db.models import Sum
from django.http import FileResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import Cart, Favorite, Ingredient, Recipe, Subscribe, Tag

from .paginators import PageLimitPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          RecipeWriteSerializer, SubscribeSerializer,
                          SubscriptionSerializer, TagSerializer)


class CustomUserViewSet(DjoserUserViewSet):

    @action(["get"], permission_classes=[IsAuthenticated], detail=False)
    def subscriptions(self, request):
        user = self.request.user
        queryset = user.subscriptions.all()
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        ["post", "delete"],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def subscribe(self, request, id):
        user = self.request.user
        if request.method == 'DELETE':
            subscribed_to = get_object_or_404(
                Subscribe,
                user=user,
                subscribed_to=id
            )
            subscribed_to.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = SubscribeSerializer(
            context={'request': self.request},
            data={'user': user.id, 'subscribed_to': id}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            queryset = user.subscriptions.all()
            serializer = SubscriptionSerializer(
                queryset,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_404_NOT_FOUND)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )
    paginator = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )
    paginator = None
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    pagination_class = PageLimitPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'create':
            return RecipeWriteSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(["get", ], permission_classes=[IsAuthenticated], detail=False)
    def download_shopping_cart(self, request):

        ingredients = Ingredient.objects.filter(
            recipes__shopping_cart__user=request.user
        ).values(
            'name',
            'measurement_unit'
        ).annotate(amount=Sum('recipe__amount')).order_by()
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        pdf.setFont('DejaVuSans', 14)
        pdf.drawString(70, 770, "Список покупок.")
        for i, ingredient in enumerate(ingredients, 1):
            pdf.drawString(
                70,
                770 - i*20,
                f"{i} "
                f"{ingredient['name']} "
                f"({ingredient['measurement_unit']}): "
                f"{ingredient['amount']}"
            )
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=False,
            filename='purchase.pdf'
        )

    def create_delete_extra(self, request, pk, model, model_field, serializer):
        user = self.request.user
        if request.method == 'DELETE':
            extra_recipe = get_object_or_404(
                model,
                user=user,
                **{model_field: pk}
            )
            extra_recipe.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = serializer(
            context={'request': self.request},
            data={'user': user.id, model_field: pk}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_404_NOT_FOUND)

    @action(
        ["post", "delete"],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def shopping_cart(self, request, pk):
        model = Cart
        model_field = 'cart_recipe'
        serializer = CartSerializer
        return self.create_delete_extra(
            request,
            pk,
            model,
            model_field,
            serializer
        )

    @action(
        ["post", "delete"],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def favorite(self, request, pk):
        model = Favorite
        model_field = 'favorite_recipe'
        serializer = FavoriteSerializer
        return self.create_delete_extra(
            request,
            pk,
            model,
            model_field,
            serializer
        )
