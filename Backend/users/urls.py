from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()

urlpatterns = [
    url('', include(routers.urls)),
    url(r'user/login/', views.LoginView.as_view()),
]