from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

#from users.views import UserViewSet
from .views import *



app_name = 'api'

router = routers.DefaultRouter()
#router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    #path('auth/token/', include('users.urls')),

]