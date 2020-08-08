from django import forms

from .models import *


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_price', 'time', 'sales']


class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'ingredient_price']


class HaveCreateForm(forms.ModelForm):
    class Meta:
        model = Have
        fields = ['proportion', 'item', 'ingredient']


class MiscellaneousCreateForm(forms.ModelForm):
    class Meta:
        model = Miscellaneous
        fields = ['miscellaneous_name', 'miscellaneous_price', 'service', 'cooking', 'sorting']