from rest_framework import serializers
from .models import Item, Ingredient, Have, Miscellaneous


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class HaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Have
        fields = '__all__'


class MiscellaneousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miscellaneous
        fields = '__all__'


