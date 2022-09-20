from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from recipes.models import User
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _


#class UserViewSet(ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    pagination_class = PageNumberPagination
#
#    @action(methods=['GET'], detail=False, url_path='me', url_name='me')
#    def me(self, request, *args, **kwargs):
#        user = self.request.user
#        serializer = self.get_serializer(user)
#        # TODO implement 'me' page
#        return Response(serializer.data)

    #@action(methods=['POST'], detail=False)
    #def set_password(self, request, *args, **kwargs):
    #    #return Response('test')
    #    serializer = PasswordChangeSerializer
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response({"detail": _("New password has been saved.")})



    #def logout(self, request):
    #    try:
    #        request.user.auth_token.delete()
    #    except (AttributeError, ObjectDoesNotExist):
    #        pass
    #
    #    logout(request)
    #
    #    return Response({"success": _("Successfully logged out.")},
    #                    status=status.HTTP_204_NO_CONTENT)


