"""
Contains the views logic that handles requests as they come
"""
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from user.serializers import (UserSerializer, AuthSerializer)


class CreateUserView(generics.CreateAPIView):
    """Handles requests for the creation of users"""
    serializer_class = UserSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginUserView(ObtainAuthToken):
    """Handles requests to login as a given user."""
    serializer_class = AuthSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
