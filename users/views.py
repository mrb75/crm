from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return self.request.user.subUsers.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, SubUsersViewPermission]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, SubUsersAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, SubUsersChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, SubUsersDeletePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            request_data = request.data
            request_data['admin'] = request.user
            user = user_serializer.create(request.data)
            return Response({'response': True, 'created_user': UserSerializer(user).data})
        else:
            return Response({'response': False, 'errors': user_serializer.errors})

    def partial_update(self, request, pk=None):
        update_instance = User.objects.get(pk=pk)
        self.check_object_permissions(request, update_instance)
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.update(
                update_instance, request.data)
            return Response({'response': True, 'updated_user': UserSerializer(user).data})
        else:
            return Response({'response': False, 'errors': user_serializer.errors})


class EditProfile(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return self.request.user

    def patch(self, request, format=None):
        user = self.get_queryset()
        profile_serializer = UserFormSerializer(data=request.data)
        if profile_serializer.is_valid():
            for idx in request.data.keys():
                if idx in ['email', 'first_name', 'last_name', 'gender', 'mobile', 'national_code']:
                    setattr(user, idx, request.data[idx])

            user.save()
            return Response({'result': True, 'user': profile_serializer.data})
        else:
            return Response({'result': False, 'response': profile_serializer.errors}, status=403)
