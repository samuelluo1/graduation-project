from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('item', views.ItemView)
routers.register('ingredient', views.IngredientView)
routers.register('have', views.HaveView)
routers.register('misc', views.MiscellaneousView)

urlpatterns = [
    url('', include(routers.urls)),
]