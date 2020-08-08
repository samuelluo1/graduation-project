from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, permissions, mixins, viewsets

from .serializers import *
from .models import *


# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class HaveViewSet(viewsets.ModelViewSet):

    queryset = Have.objects.all()
    serializer_class = HaveSerializer


class MiscellaneousViewSet(viewsets.ModelViewSet):

    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


