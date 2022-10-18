from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import *
from rest_framework.parsers import MultiPartParser
from .models import UserImage, Ticket
from django.db.models import Q
from .filters import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    filterset_class = UserFilter

    def get_queryset(self):
        return self.request.user.subUsers.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, SubUsersViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, SubUserRetrievePermission]

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
        user_serializer = UserFormSerializer(
            data=request.data, context={'request': request})
        if user_serializer.is_valid():
            # request_data = dict(**(request.data))
            # # print(request_data, request.data)
            # request_data['admin'] = request.user
            user = user_serializer.create(request.data)
            return Response({'response': True, 'created_user': UserSerializer(user).data})
        else:
            return Response({'response': False, 'errors': user_serializer.errors})

    def partial_update(self, request, pk=None):
        update_instance = User.objects.get(pk=pk)
        self.check_object_permissions(request, update_instance)
        user_serializer = UserFormSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.update(
                update_instance, request.data)
            return Response({'response': True, 'updated_user': UserSerializer(user).data})
        else:
            return Response({'response': False, 'errors': user_serializer.errors})


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, SubUsersViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, SubUserRetrievePermission]

        elif self.action == 'create':
            permission_classes = [IsAuthenticated, SubUsersAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, SubUsersChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, SubUsersDeletePermission]
        else:
            permission_classes = [IsAuthenticated]
        permission_classes.append(IsAdminPermission)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.request.user.subUsers.filter(group_name='employee_user')

    def create(self, request):
        user_serializer = UserFormSerializer(
            data=request.data, context={'request': request})
        if user_serializer.is_valid():
            # request_data = dict(**(request.data))
            # # print(request_data, request.data)
            # request_data['admin'] = request.user
            user = user_serializer.create(request.data, group='employee_user')
            return Response({'response': True, 'created_user': UserSerializer(user).data}, status=201)
        else:
            return Response({'response': False, 'errors': user_serializer.errors}, status=400)

    def partial_update(self, request, pk=None):
        update_instance = User.objects.get(pk=pk)
        self.check_object_permissions(request, update_instance)
        user_serializer = UserFormSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.update(
                update_instance, request.data)
            return Response({'response': True, 'updated_user': UserSerializer(user).data})
        else:
            return Response({'response': False, 'errors': user_serializer.errors}, status=400)


class CoworkerViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.subUsers.filter(groups__name='coworker_user')

    def get_permissions(self):

        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, SubUserRetrievePermission]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated, SubUsersChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, SubUsersDeletePermission]
        else:
            permission_classes = [IsAuthenticated]
        permission_classes.append(IsAdminPermission)
        return [permission() for permission in permission_classes]

    def create(self, request):
        user_serializer = UserFormSerializer(
            data=request.data, context={'request': request})
        if user_serializer.is_valid():
            coworker = user_serializer.create(request.data)
            coworker.groups.set([Group.objects.get(name='coworker_user')])
            return Response(self.serializer_class(coworker).data, 201)
        else:
            return Response(user_serializer.errors, 400)

    def destroy(self, request):
        return Response({}, 404)


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


class SubUserImageViewSet(viewsets.ModelViewSet):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return UserImage.objects.filter(user__admin=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, UserImageViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, UserImageRetrievePermission]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, UserImageAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, UserImageChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, UserImageDeletePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request):
        self.parser_classes = [MultiPartParser]
        sub_user = User.objects.get(pk=request.data['user'])
        self.check_object_permissions(request, sub_user)
        data = {
            'path': request.data['image'],
            'user': sub_user.id,
        }
        image_serializer = UserImageSerializer(data=data)
        if image_serializer.is_valid():
            image = UserImage.objects.create(
                user=sub_user, path=request.data['image'])
            image.save()
            image_serializer_result = UserImageSerializer(image)
            return Response({'result': True, 'created_image': image_serializer_result.data})
        else:
            return Response({'result': False, 'response': image_serializer.errors}, status=403)

    def partial_update(self, request, pk=0):
        pass

    def update(self, request):
        pass

    def destroy(self, request, pk=0):
        self.check_object_permissions(request, UserImage.objects.get(pk=pk))
        image = UserImage.objects.get(pk=pk)
        image.delete()
        return Response({'result': True})


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return self.request.user.tickets.all()

    def list(self, request):
        return Response({'result': True, 'data': self.queryset})

    # def retrieve(self, request, pk=0):
    #     ticket = Ticket.objects.get(pk=pk)
    #     self.check_object_permissions(request, ticket)
    #     return Response({'result': True, 'data': TicketSerializer(ticket).data})

    def create(self, request):
        ticket_serializer = TicketFormSerializer(data=request.data)
        if ticket_serializer.is_valid():
            request_data = request.data
            request_data['user'] = request.user
            ticket = ticket_serializer.create(request_data)
            return Response({'result': True, 'created_ticket': TicketSerializer(ticket).data}, status=201)
        else:
            return Response({'result': False, 'response': ticket_serializer.errors}, status=403)

    def partial_update(self, request, pk=0):
        self.check_object_permissions(request, Ticket.objects.get(pk=pk))
        super().partial_update(request, pk)

    def destroy(self, request, pk=0):
        self.check_object_permissions(request, Ticket.objects.get(pk=pk))
        super().destroy(request, pk)


class AdminTicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return Ticket.objects.filter(Q(user__admin=self.request.user) | Q(user__admin=self.request.user.admin))

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, TicketViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, TicketRetrievePermission]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, TicketAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, TicketChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, TicketRemovePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class UserPermissions(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = PermissionSerializer

    def get_queryset(self, pk):
        user = self.request.user.subUsers.get(pk=pk)
        return Permission.objects.filter(user=user)

    def get(self, request, pk):
        # print(self.get_queryset(pk))
        return Response({'data': self.serializer_class(self.get_queryset(pk), many=True).data})


class ChangeUserPermissions(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self, pk):
        return self.request.user.subUsers.get(pk=pk)

    def patch(self, request, pk):
        user = self.get_queryset(pk)
        permission_serializer = PermissionSetSerializer(
            data=request.data)
        if permission_serializer.is_valid():
            user.user_permissions.set(request.data['permission_id'])
            return Response(status=204)
        else:
            return Response({'errors': permission_serializer.errors}, status=400)


class TurnReadViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = TurnSerializer

    def get_queryset(self):
        return Turn.objects.filter(Q(user__admin=self.request.user) | Q(user__admin=self.request.user.admin))

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, TurnViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, TurnRetrievePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class TurnViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = TurnFormSerializer

    def get_queryset(self):
        return Turn.objects.filter(Q(user__admin=self.request.user) | Q(user__admin=self.request.user.admin))

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, TurnViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, TurnRetrievePermission]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, TurnAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, TurnChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, TurnRemovePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
