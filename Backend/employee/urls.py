from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('employee', views.EmployeeView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^get_employee', views.EmployeeGetApiView.as_view()),
    url(r'^post_employee', views.EmployeePostApiView.as_view()),
    url(r'^put_employee', views.EmployeePutApiView.as_view()),
]