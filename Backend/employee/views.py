from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import EmployeeSerializer
from .models import Employee
from django.contrib.auth.models import User


class EmployeeView(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeGetApiView(generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, format=None):
        user = Employee.objects.filter(user=User.objects.get(username=request.session['username']).pk)
        serializer = EmployeeSerializer(user, many=True)
        return Response(serializer.data, HTTP_200_OK)


class EmployeePostApiView(generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def post(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('新增成功', status=HTTP_200_OK)
        return Response("新增失敗", status=HTTP_400_BAD_REQUEST)


class EmployeePutApiView(generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def put(self, request, format=None):
        request.data["user"] = User.objects.get(username=request.session['username']).pk

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('更新成功', status=HTTP_200_OK)
        return Response("更新失敗", status=HTTP_400_BAD_REQUEST)
