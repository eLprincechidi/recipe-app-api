from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingredient,
)



class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'description', 'price', 'link', 'tags',
            'ingredients',
            ]
        read_only_fields = ['id', 'user']


    def _get_or_create_tags(self, tags_data, instance):
        auth_user = self.context['request'].user
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(user=auth_user, **tag_data)
            instance.tags.add(tag)

    def _get_or_create_ingredients(self, ingredients_data, instance):
        """Handles getting or creating ingredients as needed."""
        auth_user = self.context['request'].user
        for ingredient_data in ingredients_data:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient_data
            )
            instance.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags_data, recipe)
        self._get_or_create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Only touch tags if the key was present in the request
        if tags_data is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags_data, instance)

        # Only touch ingredients if the key was present in the request
        if ingredients_data is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients_data, instance)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()


        return instance



class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""
    tags = TagSerializer(many=True, required=False)


    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}


