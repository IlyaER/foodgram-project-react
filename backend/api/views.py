from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from recipes.models import User
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @action(methods=['GET'], detail=False, url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        # TODO implement 'me' page
        return Response('test')



