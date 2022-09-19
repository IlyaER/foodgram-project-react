from django.contrib.auth import authenticate
from rest_auth.models import TokenModel
from rest_auth.serializers import TokenSerializer
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


class EmailAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'email', 'password', 'user'

class AuthTokenSerializer(TokenSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = TokenModel
        fields = ('auth_token',)

#class EmailAuthTokenSerializer(serializers.Serializer):
#
#    email = serializers.CharField(
#        label=_("Email"),
#        write_only=True
#    )
#    password = serializers.CharField(
#        label=_("Password"),
#        style={'input_type': 'password'},
#        trim_whitespace=False,
#        write_only=True
#    )
#    token = serializers.CharField(
#        label=_("Token"),
#        read_only=True
#    )
#
#    def validate(self, attrs):
#        email = attrs.get('email')
#        password = attrs.get('password')
#        username = serializers.SlugRelatedField(
#            slug_field='username', many=False, queryset=User.objects.all()
#        )
#
#        if email and password:
#            user = authenticate(request=self.context.get('request'),
#                                username=username, password=password)
#
#            # The authenticate call simply returns None for is_active=False
#            # users. (Assuming the default ModelBackend authentication
#            # backend.)
#            if not user:
#                msg = _('Unable to log in with provided credentials.')
#                raise serializers.ValidationError(msg, code='authorization')
#        else:
#            msg = _('Must include "username" and "password".')
#            raise serializers.ValidationError(msg, code='authorization')
#
#        attrs['user'] = user
#        return attrs
