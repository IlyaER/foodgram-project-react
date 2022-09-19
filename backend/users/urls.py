from django.urls import include, path
from rest_auth.views import LoginView, LogoutView
from rest_framework import routers
from rest_framework.authtoken import views

from .views import *


app_name = 'users'

router = routers.DefaultRouter()


urlpatterns = [
    path('', include('rest_auth.urls')),
    #path('login/', LoginView.as_view(), name='rest_login'),
    path('login/', TokenLoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    #path('login/', AuthToken.as_view()),
    #path('login/', views.obtain_auth_token),
    # TODO implement customized ObtainAuthToken
]
