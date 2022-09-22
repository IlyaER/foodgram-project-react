from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import *
from users.serializers import UserSerializer
import base64


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')






class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SlugRelatedField(
        slug_field='recipe',
        queryset=Ingredients.objects.all(),
        read_only=True
    )
    class Meta:
        model = Ingredients
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    #measurement_unit = IngredientSerializer(source='name')
    measurement_unit = serializers.SlugRelatedField(
        source='name',
        slug_field='measurement_unit',
        #queryset=Ingredients.objects.all(),
        read_only=True,
    )

    class Meta:
        model = RecipeIngredients
        #fields = '__all__'
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('measurement_unit',)

        extra_kwargs = {
                    'name': {'source': 'id', 'write_only': True},
                    #'id': {'write_only': True}
                }




class RecipeSerializer(serializers.ModelSerializer):
    #author = serializers.SlugRelatedField(
    #    slug_field='username', read_only=True
    #)
    author = UserSerializer(read_only=True)
    #ingredients = RecipeIngredientSerializer(source='ingredients_to', many=True)
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        #fields = '__all__'
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time',)
        # TODO "is_favorited": true, "is_in_shopping_cart": true,

    def validate(self, data):
        print(data)
        return data


    #def create(self, validated_data):
    #    return validated_data


class SubscribeSerializer(serializers.ModelSerializer):
    #subscribed_to = serializers.SlugRelatedField(
    #    slug_field='username',
    #    queryset=User.objects.all()
    #)
    subscribed_to = UserSerializer(read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('user', 'subscribed_to')
        model = Subscribe

    def create(self, validated_data):
        return Subscribe.objects.create(**validated_data)

    def validate(self, data):
        user = self.context['request'].user
        subscribe = data['subscribed_to']
        if user == subscribe:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя"
            )
        if Subscribe.objects.filter(
                user=user,
                subscribed_to=subscribe
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора"
            )
        return data
