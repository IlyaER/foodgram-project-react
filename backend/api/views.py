from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from recipes.models import User

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


