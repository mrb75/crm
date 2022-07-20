from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'usersImage', SubUserImageViewSet, basename='userImage')

urlpatterns = [
    path('EditProfile', EditProfile.as_view()),
]

urlpatterns += router.urls
