from django.shortcuts import render
from rest_framework import generics
from status import serializers
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from status.models import Status
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import login

# Create your views here.
class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [
        permissions.AllowAny 
    ]
class Login(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    def post(self, request, format=None):
        
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key},
                    status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class statusUpload(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = serializers.StatusSerializer

    def perform_create(self, serializer):
        
        serializer.save(owner=self.request.user)

class StatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = serializers.StatusSerializer
