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
    #amount = serializers.SlugRelatedField(
    #    source='*',
    #    slug_field='amount',
    #    #queryset=Ingredients.objects.all(),
    #    read_only=True
    #)
    #amount = "RecipeIngredientSerializer(source='ingredients_to')"
    #amount = serializers.PrimaryKeyRelatedField(
    #    queryset=RecipeIngredients.objects.all(),
    #    #source='name_id'
    #)
    amount = serializers.CharField(read_only=True, source='name.amount')
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
        #read_only_fields = ('id', 'measurement_unit',)

        #extra_kwargs = {
        #            'name': {'source': 'id', 'write_only': True},
        #            #'id': {'write_only': True}
        #        }

    def validate(self, attrs):
        print(f'RecipeIngred Attrs: {attrs}')
        #print(f'RecipeIngred Attrs: {self.initial_data}')
        return attrs

class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    #id = serializers.SlugRelatedField(
    #    slug_field='id',
    #    source='name',
    #    #read_only=True
    #    queryset=Ingredients.objects.all()
    #)
    id = serializers.PrimaryKeyRelatedField(source='name', queryset=Ingredients.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('amount', 'id',)
        #extra_kwargs = {
        #    'name': {'source': 'id',}# 'write_only': True},
        #    #'id': {'write_only': True},
        #}

class RecipeWriteSerializer(serializers.ModelSerializer):
    #author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientWriteSerializer(source='ingredients_to', many=True)
    #tags = TagSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'name', 'image', 'text', 'cooking_time',)#'__all__', )

    #def validate(self, attrs):
    #    print(f'Attrs: {attrs}')
    #    print(self.initial_data)
    #    return attrs

    def create(self, validated_data):
        print(f'Initial data: {self.initial_data}')
        print(f'Validated data: {validated_data}')
        ingredients = validated_data.pop('ingredients_to')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        print(ingredients)
        print(recipe)
        print(tags)
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                **ingredient, recipe_id=recipe.id)
        for tag in tags:
            RecipesTags.objects.create(**tag, recipe_id=recipe.id)
        return recipe #validated_data


class RecipeSerializer(serializers.ModelSerializer):
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    if 'request' in self.context and self.context['request'].method == 'GET':
    #        self.fields['is_favorited'] = serializers.SerializerMethodField(read_only=True)
    #        self.fields['is_in_shopping_cart'] = serializers.SerializerMethodField(read_only=True)

    #author = serializers.SlugRelatedField(
    #    slug_field='username', read_only=True
    #)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(source='ingredients_to', many=True)
    #ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        #fields = '__all__'
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')
        read_only_fields = ('id', 'is_favorited', 'is_in_shopping_cart')
        #extra_kwargs = {
        #    'ingredients': {'source': 'recipes', 'write_only': True},
        #}

    def get_is_favorited(self, obj):
    #    pass
        if 'request' in self.context and self.context['request'].method != 'GET':
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(favorite_recipe_id=obj.id).exists()


    def get_is_in_shopping_cart(self, obj):
    #    pass
        if 'request' in self.context and self.context['request'].method != 'GET':
            return False
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(cart_recipe_id=obj.id).exists()


    def validate(self, attrs):
        print(f'Attrs: {attrs}')
        print(self.initial_data)
        return attrs


    def create(self, validated_data):
        print(f'Initial data: {self.initial_data}')
        print(f'Validated data: {validated_data}')
        return validated_data


class ShortRecipeSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')





class SubscriptionSerializer(UserSerializer):
    recipes = ShortRecipeSerializer(source='recipe', many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = 'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        read_only_fields = 'id', 'is_subscribed',

    def get_recipes_count(self, obj):
        return obj.recipe.count()


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'

    #def create(self, validated_data):
    #    return Subscribe.objects.create(**validated_data)

    def validate(self, data):
        user = self.context['request'].user
        subscribed_to = data['subscribed_to']
        if user == subscribed_to:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя"
            )
        if Subscribe.objects.filter(
                user=user,
                subscribed_to=subscribed_to
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора"
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
                "Рецепт уже в избранном"
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
                "Рецепт уже в корзине"
            )
        return data
