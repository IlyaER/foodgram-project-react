from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.utils import model_meta

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


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    #amount = serializers.PrimaryKeyRelatedField(
    #    queryset=RecipeIngredients.objects.all(),
    #    #source='name_id'
    #)
    amount = serializers.CharField(read_only=True, source='name.amount')
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        slug_field='ingredient',
        read_only=True
    )

    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        #fields = '__all__'
        fields = ('id', 'name', 'measurement_unit', 'amount')


    def validate(self, attrs):
        print(f'RecipeIngred Attrs: {attrs}')
        #print(f'RecipeIngred Attrs: {self.initial_data}')
        return attrs

class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


#class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
#    id = serializers.SlugRelatedField(
#        slug_field='id',
#        source='name',
#        #read_only=True
#        queryset=Ingredients.objects.all()
#    )
#    #id = serializers.PrimaryKeyRelatedField(source='name', queryset=Ingredients.objects.all(), write_only=True)
#
#    class Meta:
#        model = RecipeIngredients
#        fields = ('amount', 'id',)


class RecipeWriteSerializer(serializers.ModelSerializer):
    #ingredients = RecipeIngredientWriteSerializer(source='ingredients_to', many=True)
    ingredients = RecipeIngredientWriteSerializer(many=True)
    #tags = TagSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'name', 'image', 'text', 'cooking_time',)#'__all__', )


    def create(self, validated_data):
        print(f'Initial data: {self.initial_data}')
        print(f'Validated data: {validated_data}')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        print(f'ingredients {ingredients}')
        print(recipe)
        print(tags)
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                **ingredient, recipe_id=recipe.id)
        for tag in tags:
            RecipesTags.objects.create(tag=tag, recipe_id=recipe.id)
        print(f'Recipe: {recipe}')
        return recipe #validated_data


    def update(self, instance, validated_data):
        instance.image = validated_data.get(
            'image', instance.image)
        instance.name = validated_data.get(
            'name', instance.name)
        print(instance.tags)
        print(validated_data)
        if validated_data.get('tags'):
            instance.tags.clear()
            instance.tags.set(validated_data.pop('tags'))

            #tags = validated_data.pop('tags')
            #for tag in tags:
            #    RecipesTags.objects.create(tag=tag, recipe_id=instance.id)
        print(instance.tags)
        if validated_data.get('ingredients'):
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            elements = []
            for ingredient in ingredients:
                elements.append(
                    RecipeIngredients(
                        recipe=instance,
                        name_id=ingredient.get("id"),
                        amount=ingredient.get("amount"),
                    )
                )
            RecipeIngredients.objects.bulk_create(elements)
        #    #TODO some strange things with ingredients
        #    # #instance.ingredients_to.clear()
        #    #RecipeIngredients.objects.filter(recipe=instance).all().delete()
        #    ingredients = validated_data.pop('ingredients_to')
        #    print(ingredients)
        #    for ingredient in ingredients:
        #        print(instance.id, ingredient)
        #        amount = ingredient['amount']
        #        #RecipeIngredients.objects.update_or_create(
        #        #    ingredient['name'],
        #        #    amount=amount,
        #        #    recipe_id=instance.id
        #        #)
        #        ingredient = RecipeIngredients.objects.get_or_create(pk=ingredient['name'].id)
        #        print(ingredient)
        #        RecipeIngredients.objects.update_or_create(#amount=amount,
        #            **ingredient[0], )#recipe_id=instance.id)
        #    #RecipeIngredients.objects.create(**ingredients)#, recipe_id=recipe.id)
        #    #instance.ingredients.set(validated_data.pop('ingredients_to'))
        print(f'Last validated data: {validated_data}')
        instance.save()
        #recipe = Recipe.objects.update(**validated_data)
        #print(f'Recipe: {recipe}')
        return instance


class RecipeSerializer(serializers.ModelSerializer):
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
