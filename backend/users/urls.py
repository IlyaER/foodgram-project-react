from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

#from .views import *


app_name = 'users'

router = routers.DefaultRouter()


urlpatterns = [
    path('', include('djoser.urls.authtoken')),
    #path('login/', LoginView.as_view(), name='rest_login'),
    #path('logout/', LogoutView.as_view(), name='rest_logout'),
]
