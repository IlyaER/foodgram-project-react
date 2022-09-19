from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from recipes.models import User
from .serializers import UserSerializer, EmailAuthTokenSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @action(methods=['GET'], detail=False, url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        # TODO implement 'me' page
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def set_password(self, request, *args, **kwargs):
        return Response('test')



class AuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

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


