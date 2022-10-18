from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'coworkers', CoworkerViewSet, basename='coworker')
router.register(r'usersImage', SubUserImageViewSet, basename='userImage')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'adminTickets', AdminTicketViewSet, basename='adminTicket')
router.register(r'turns', TurnViewSet, basename='turn')
router.register(r'readTurns', TurnReadViewSet, basename='readTurn')

urlpatterns = [
    path('EditProfile', EditProfile.as_view()),
    path('UserPermissionList/<int:pk>', UserPermissions.as_view()),
    path('ChangeUserPermissionList/<int:pk>', ChangeUserPermissions.as_view()),
]

urlpatterns += router.urls
