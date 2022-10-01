from django.urls import include, path
from rest_framework import routers

app_name = 'users'

router = routers.DefaultRouter()


urlpatterns = [
    path('', include('djoser.urls.authtoken')),
]
