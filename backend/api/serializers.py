import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, RecipeTag, Subscribe, Tag)
from users.models import User
from users.serializers import UserSerializer


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


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.CharField(read_only=True, source='name.amount')

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientWriteSerializer(
        many=True,
        source='ingredient'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
                recipe=recipe
            )
        for tag in tags:
            RecipeTag.objects.create(tag=tag, recipe_id=recipe.id)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get(
            'image', instance.image)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.text = validated_data.get(
            'text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        if validated_data.get('tags'):
            instance.tags.clear()
            tags = validated_data.pop('tags')
            for tag in tags:
                RecipeTag.objects.create(tag=tag, recipe_id=instance.id)
        ingredients = validated_data.pop('ingredient')
        instance.ingredients.clear()
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
                recipe=instance
            )
        instance.save()
        return instance


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, source='ingredient')
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )
        read_only_fields = ('id', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        method = self.context['request'].method
        if 'request' in self.context and method != 'GET':
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(favorite_recipe_id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        method = self.context['request'].method
        if 'request' in self.context and method != 'GET':
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(cart_recipe_id=obj.id).exists()


class ShortRecipeSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(UserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = 'id', 'is_subscribed',

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipe.count()


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        subscribed_to = data['subscribed_to']
        if user == subscribed_to:
            raise serializers.ValidationError(
                "???????????? ?????????????????????? ???? ???????????? ????????"
            )
        if Subscribe.objects.filter(
                user=user,
                subscribed_to=subscribed_to
        ).exists():
            raise serializers.ValidationError(
                "???? ?????? ?????????????????? ???? ?????????? ????????????"
            )
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        favorite_recipe = data['favorite_recipe']
        if Favorite.objects.filter(
                user=user,
                favorite_recipe=favorite_recipe
        ).exists():
            raise serializers.ValidationError(
                "???????????? ?????? ?? ??????????????????"
            )
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        cart_recipe = data['cart_recipe']
        if Cart.objects.filter(
                user=user,
                cart_recipe=cart_recipe
        ).exists():
            raise serializers.ValidationError(
                "???????????? ?????? ?? ??????????????"
            )
        return data
