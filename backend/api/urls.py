from django.urls import include, path
from rest_auth.views import PasswordChangeView
from rest_framework import routers
from rest_framework.authtoken import views

from users.views import UserViewSet
from .views import *


app_name = 'api'

router = routers.DefaultRouter()
#router.register('users', UserViewSet, basename='users')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', include('users.urls')),
    path('users/set_password/', PasswordChangeView.as_view(),
        name='rest_password_change'),

]