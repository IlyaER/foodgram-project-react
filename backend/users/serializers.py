from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _


from recipes.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = 'email', 'id', 'username', 'first_name', 'last_name', # TODO 'is_subscribed', 'password' (not shown)
        read_only_fields = 'id',



