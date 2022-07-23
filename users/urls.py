from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'usersImage', SubUserImageViewSet, basename='userImage')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('EditProfile', EditProfile.as_view()),
]

urlpatterns += router.urls
