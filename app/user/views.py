# from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


# Create your views here.
# view for managing our create user api
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token t=for user"""
    serializers_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.CreateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # class variables for authentication and permission
    authentication_class = (authentication.TokenAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    # typically you link APIView and retrieve database models
    # In this case, we retrieve the model for the logged in user, overwrite the get_object()
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user    # takes care of the authenticated user and assigning it to request
