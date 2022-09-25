import debug_toolbar
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views


from foodgram import settings
from .views import *



app_name = 'api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    #path('', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),

    path('auth/', include('users.urls')),
]

urlpatterns += router.urls

