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
    url(r'^get_item', views.ItemGetApiView.as_view()),
    url(r'^post_item', views.ItemPostApiView.as_view()),
    url(r'^put_item', views.ItemPutApiView.as_view()),
    url(r'^get_ingredient', views.IngredientGetApiView.as_view()),
    url(r'^post_ingredient', views.IngredientPostApiView.as_view()),
    url(r'^put_ingredient', views.IngredientPutApiView.as_view()),
    url(r'^get_have', views.HaveGetApiView.as_view()),
    url(r'^post_have', views.HavePostApiView.as_view()),
    url(r'^put_have', views.HavePutApiView.as_view()),
    url(r'^get_misc', views.MiscellaneousGetApiView.as_view()),
    url(r'^post_misc', views.MiscellaneousPostApiView.as_view()),
    url(r'^put_misc', views.MiscellaneousPutApiView.as_view()),
]