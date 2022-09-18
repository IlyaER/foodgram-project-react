from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import *


app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
]