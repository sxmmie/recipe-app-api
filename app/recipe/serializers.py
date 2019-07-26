from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tsg object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = {'id', 'name'}
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    #
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()   # list ingredients with their primary key id
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()   # list tags with their primary key id
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'price',
                  'time_minutes', 'tags', 'ingredients', 'link')
        read_only = ('id',)


# Base this serializer off the RecipeSerializer
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for each recipe object"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
