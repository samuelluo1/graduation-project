from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .serializers import ItemSerializer, IngredientSerializer, HaveSerializer, MiscellaneousSerializer
from .models import Item, Ingredient, Have, Miscellaneous


class ItemView(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class IngredientView(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class HaveView(viewsets.ModelViewSet):

    queryset = Have.objects.all()
    serializer_class = HaveSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("ingredient", "item",)


class MiscellaneousView(viewsets.ModelViewSet):

    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


