from rest_framework import serializers

from recipes.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = 'email', 'id', 'username', 'first_name', 'last_name', # TODO 'is_subscribed', 'password' (not shown)
        read_only_fields = 'id',

