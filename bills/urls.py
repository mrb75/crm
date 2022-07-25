from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bill')

urlpatterns = [
]

urlpatterns += router.urls
