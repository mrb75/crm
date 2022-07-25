from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Bill
from rest_framework.response import Response


class BillViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = BillSerializer

    def get_queryset(self):
        return Bill.objects.filter(user__admin=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, BillViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, BillRetrievePermission]

        elif self.action == 'create':
            permission_classes = [IsAuthenticated, BillAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, BillChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, BillDeletePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=0):
        bill = Bill.objects.get(pk=pk)
        self.check_object_permissions(request, bill)
        return super().retrieve(request, pk=pk)

    def partial_update(self, request, pk=0):
        bill = Bill.objects.get(pk=pk)
        self.check_object_permissions(request, bill)
        return super().partial_update(request, pk=pk)

    def destroy(self, request, pk=0):
        bill = Bill.objects.get(pk=pk)
        self.check_object_permissions(request, bill)
        return super().destroy(request, pk=pk)
