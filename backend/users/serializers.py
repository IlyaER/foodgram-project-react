from rest_framework import serializers

from recipes.models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = 'id', 'is_subscribed'

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return not user.is_anonymous and user.subscriptions.filter(id=obj.id).exists()
