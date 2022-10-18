from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import Permission, Group
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class SetUpTestCase(APITestCase):

    def setUp(self):
        admin_permissions = Permission.objects.filter(codename__in=[
            'view_user', 'add_user', 'change_user', 'delete_user',
            'view_userimage', 'add_userimage', 'change_userimage', 'delete_userimage',
            'view_notification', 'add_notification', 'change_notification', 'delete_notification',
            'view_notificationtype', 'add_notificationtype', 'change_notificationtype', 'delete_notificationtype',
            'view_turn', 'add_turn', 'change_turn', 'delete_turn',
            'view_ticket', 'add_ticket', 'change_ticket', 'delete_ticket',
        ])
        employee_permissions = Permission.objects.filter(
            codename__in=['view_ticket', 'add_ticket', 'change_ticket', 'delete_ticket'])
        end_permissions = Permission.objects.filter(
            codename__in=['view_userimage', 'add_userimage', 'change_userimage', 'delete_userimage', 'view_ticket', 'add_ticket', 'change_ticket', 'delete_ticket'])
        g_admin = Group.objects.create(name='admin_user')
        g_employee = Group.objects.create(name='employee_user')
        g_coworker = Group.objects.create(name='coworker_user')
        g_end = Group.objects.create(name='end_user')
        g_admin.permissions.set(admin_permissions)
        g_employee.permissions.set(employee_permissions)
        g_end.permissions.set(end_permissions)
        self.u_admin = User.objects.create(
            username='u_admin', password='mmmmm46456456456')
        self.u_admin.groups.add(Group.objects.get(name='admin_user'))
        self.u_employee = User.objects.create(
            username='u_employee', password='mmmmm46456456456', admin=self.u_admin)
        self.u_employee.groups.add(Group.objects.get(name='employee_user'))
        self.u_coworker = User.objects.create(
            username='u_coworker', password='mmmmm46456456456', admin=self.u_admin)
        self.u_coworker.groups.set([Group.objects.get(name='employee_user')])
        self.u_end = User.objects.create(
            username='u_end', password='mmmmm46456456456', admin=self.u_admin)
        self.u_end.groups.add(Group.objects.get(name='end_user'))

    def _jwt_auth(self, user):
        refresh_token = RefreshToken().for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))


class UserStatisticsTest(SetUpTestCase):
    def test_can_get_users_per_month(self):
        super()._jwt_auth(self.u_admin)
        r_user_stat_get = self.client.get(
            '/api/statInfo/userStatistics/per_month_created_user', format='json')
        self.assertEqual(r_user_stat_get.status_code, 200)
