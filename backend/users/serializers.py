from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _


from recipes.models import *


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        #fields = '__all__'
        fields = 'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', # TODO is subscribed
        read_only_fields = 'id',

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.subscriptions.filter(id=obj.id).exists()



