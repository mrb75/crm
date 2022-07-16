from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return self.request.user.subUsers.all()


class EditProfile(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return self.request.user

    def patch(self, request, format=None):
        user = self.get_queryset()
        profile_serializer = EditProfile(data=request.data)
        if profile_serializer.is_valid():
            user.email = profile_serializer.data['email']
            user.mobile = profile_serializer.data['mobile']
            user.national_code = profile_serializer.data['national_code']
            user.gender = profile_serializer.data['gender']
            user.username = profile_serializer.data['username']
            user.first_name = profile_serializer.data['first_name']
            user.last_name = profile_serializer.data['last_name']
            user.save()
            return Response({'result': True, 'user': profile_serializer.data})
        else:
            return Response({'result': False, 'response': profile_serializer.errors}, status=403)
