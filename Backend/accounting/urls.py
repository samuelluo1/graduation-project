from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'item', ItemViewSet)
router.register(r'ingredient', IngredientViewSet)
router.register(r'have', HaveViewSet)
router.register(r'misc', MiscellaneousViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),

]