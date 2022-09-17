from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from recipes.models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
