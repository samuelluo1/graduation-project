from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('employee', views.EmployeeView)

urlpatterns = [
    url('', include(routers.urls)),
]