from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import ItemSerializer, IngredientSerializer, HaveSerializer, MiscellaneousSerializer
from .models import Item, Ingredient, Have, Miscellaneous
from django.contrib.auth.models import User


class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemGetApiView(generics.GenericAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, format=None):
        user = Item.objects.filter(user=User.objects.get(username=request.session['username']).pk)
        serializer = ItemSerializer(user, many=True)
        return Response(serializer.data, HTTP_200_OK)


class ItemPostApiView(generics.GenericAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def post(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response("新增失敗", status=HTTP_400_BAD_REQUEST)


class ItemPutApiView(generics.GenericAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def put(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('更新成功', status=HTTP_200_OK)
        return Response("更新失敗", status=HTTP_400_BAD_REQUEST)


class IngredientView(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientGetApiView(generics.GenericAPIView):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get(self, request, format=None):
        user = Ingredient.objects.filter(user=User.objects.get(username=request.session['username']).pk)
        serializer = IngredientSerializer(user, many=True)
        return Response(serializer.data, HTTP_200_OK)


class IngredientPostApiView(generics.GenericAPIView):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def post(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response("新增失敗", status=HTTP_400_BAD_REQUEST)


class IngredientPutApiView(generics.GenericAPIView):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def put(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('更新成功', status=HTTP_200_OK)
        return Response("更新失敗", status=HTTP_400_BAD_REQUEST)


class HaveView(viewsets.ModelViewSet):

    queryset = Have.objects.all()
    serializer_class = HaveSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("ingredient", "item",)


class HaveGetApiView(generics.GenericAPIView):

    queryset = Have.objects.all()
    serializer_class = HaveSerializer

    def get(self, request, format=None):
        user = Have.objects.filter(user=User.objects.get(username=request.session['username']).pk)
        serializer = HaveSerializer(user, many=True)
        return Response(serializer.data, HTTP_200_OK)


class HavePostApiView(generics.GenericAPIView):

    queryset = Have.objects.all()
    serializer_class = HaveSerializer

    def post(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = HaveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('新增成功', status=HTTP_200_OK)
        return Response("新增失敗", status=HTTP_400_BAD_REQUEST)


class HavePutApiView(generics.GenericAPIView):

    queryset = Have.objects.all()
    serializer_class = HaveSerializer

    def put(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = HaveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('更新成功', status=HTTP_200_OK)
        return Response("更新失敗", status=HTTP_400_BAD_REQUEST)


class MiscellaneousView(viewsets.ModelViewSet):

    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


class MiscellaneousGetApiView(generics.GenericAPIView):

    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer

    def get(self, request, format=None):
        user = Miscellaneous.objects.filter(user=User.objects.get(username=request.session['username']).pk)
        serializer = MiscellaneousSerializer(user, many=True)
        return Response(serializer.data, HTTP_200_OK)


class MiscellaneousPostApiView(generics.GenericAPIView):

    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer

    def post(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = MiscellaneousSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('新增成功', status=HTTP_200_OK)
        return Response("新增失敗", status=HTTP_400_BAD_REQUEST)


class MiscellaneousPutApiView(generics.GenericAPIView):

    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer

    def put(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = MiscellaneousSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('更新成功', status=HTTP_200_OK)
        return Response("更新失敗", status=HTTP_400_BAD_REQUEST)
