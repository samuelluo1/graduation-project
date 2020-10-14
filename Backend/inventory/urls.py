from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('inventory', views.InventoryView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^get_inventory', views.InventoryGetApiView.as_view()),
    url(r'^post_inventory', views.InventoryPostApiView.as_view()),
    url(r'^put_inventory', views.InventoryPutApiView.as_view()),
]