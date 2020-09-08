from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('inventory', views.InventoryView)

urlpatterns = [
    url('', include(routers.urls)),
]