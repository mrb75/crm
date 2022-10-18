from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *
router = DefaultRouter()

urlpatterns = [
    path('userStatistics/<str:name>', UserStatisticsView.as_view()),
    path('billStatistics/<str:name>', BillStatisticsView.as_view()),
]

urlpatterns += router.urls
