from rest_framework import serializers

from recipes.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

