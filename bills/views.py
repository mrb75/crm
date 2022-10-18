from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Bill
from rest_framework.response import Response
from django.db.models import Q


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

    def create(self, request):
        bill_form_serializer = BillFormSerializer(
            data=request.data, context={'request': request})
        if bill_form_serializer.is_valid():
            bill = bill_form_serializer.create(request.data, request.user)
            return Response({'created_bill': BillSerializer(bill).data}, status=201)
        else:
            return Response({'response': bill_form_serializer.errors}, status=400)

    def partial_update(self, request, pk=0):
        bill = Bill.objects.get(pk=pk)
        self.check_object_permissions(request, bill)
        return super().partial_update(request, pk=pk)

    def destroy(self, request, pk=0):
        bill = Bill.objects.get(pk=pk)
        self.check_object_permissions(request, bill)
        return super().destroy(request, pk=pk)


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(Q(user=self.request.user)|Q(user=self.request.user.admin))

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, CategoryViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, CategoryRetrievePermission]

        elif self.action == 'create':
            permission_classes = [IsAuthenticated, CategoryAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, CategoryChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, CategoryRemovePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request):
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category = category_serializer.create(request.data, request.user)
            return Response({'created_category': CategorySerializer(category).data}, status=201)
        else:
            return Response({'errors': category_serializer.errors}, status=400)

    def destroy(self, request, pk=0):
        category = Category.objects.get(pk=pk)
        self.check_object_permissions(request, category)
        return super().destroy(request, pk=pk)


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(Q(user=self.request.user) | Q(category__user=self.request.user))

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ProductViewPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ProductRetrievePermission]

        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ProductAddPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, ProductChangePermission]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, ProductRemovePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request):
        product_serializer = ProductFormSerializer(data=request.data)
        if product_serializer.is_valid():
            product = product_serializer.create(request.data)
            return Response({'created_product': ProductSerializer(product).data}, status=201)
        else:
            return Response({'errors': product_serializer.errors}, status=400)
