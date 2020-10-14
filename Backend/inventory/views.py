from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import InventorySerializer
from .models import Inventory
from django.contrib.auth.models import User


class InventoryView(viewsets.ModelViewSet):

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryGetApiView(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request, format=None):
        user = Inventory.objects.filter(user=User.objects.get(username=request.session['username']).pk)
        serializer = InventorySerializer(user, many=True)
        return Response(serializer.data, HTTP_200_OK)


class InventoryPostApiView(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def post(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('新增成功', status=HTTP_200_OK)
        return Response("新增失敗", status=HTTP_400_BAD_REQUEST)


class InventoryPutApiView(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def put(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('更新成功', status=HTTP_200_OK)
        return Response("更新失敗", status=HTTP_400_BAD_REQUEST)
