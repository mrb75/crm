from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken


class UrlTest(APITestCase):

    def setUp(self):
        self.u_admin = User.objects.create(
            username='u_admin', password='Mrb76420')
        self.u_admin.groups.add(Group.objects.get(name='admin_user'))
        self.u_employee = User.objects.create(
            username='u_employee', password='Mrb76420', admin=self.u_admin)
        self.u_employee.groups.add(Group.objects.get(name='employee_user'))
        self.u_end = User.objects.create(
            username='u_end', password='Mrb76420', admin=self.u_admin)
        self.u_end.groups.add(Group.objects.get(name='end_user'))

    def __jwt_auth(self, user):
        refresh_token = RefreshToken().for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))
        self.expected_status_users = 200 if user.has_perm(
            'users.view_user') else 403
        self.expected_status_users_add = 200 if user.has_perm(
            'users.add_user') else 403
        self.expected_status_users_change = 200 if user.has_perm(
            'users.change_user') else 403

    def test_users_url(self):
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            r_users = self.client.get('/api/users/users/', format='json')
            self.assertEqual(r_users.status_code,
                             self.expected_status_users)

    def test_can_create_users(self):
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            create_user_data = {
                'username': 'test_'+user.username,
                'fist_name': 'test',
                'last_name': 'testian',
                'email': 'test@test.test',
                'gender': 'Male',
            }
            r_users_add = self.client.post(
                '/api/users/users/', data=create_user_data, format='json')
            self.assertEqual(r_users_add.status_code,
                             self.expected_status_users_add)

    def test_can_change_own_sub_users(self):
        for user in [self.u_admin, self.u_employee]:
            self.__jwt_auth(user)
            if user == self.u_employee:
                sub_user = user.admin.subUsers.all()[0]
            else:
                sub_user = user.subUsers.all()[0]
            r_users_change = self.client.patch(
                '/api/users/users/'+str(sub_user.id)+'/', data={'username': 'test2', 'fist_name': 'test2', 'last_name': 'testian2'}, format='json')
            self.assertEqual(r_users_change.status_code,
                             200)

    def test_cant_change_other_sub_users(self):
        other_admin = User.objects.create(
            username='u_other_admin', password='Mrb76420')

        other_admin.groups.add(Group.objects.get(name='admin_user'))
        sub_user = User.objects.create(
            username='u_other_admin_sub', password='Mrb76420')
        other_admin.subUsers.set([sub_user])
        self.__jwt_auth(self.u_admin)
        r_users_change = self.client.patch(
            '/api/users/users/'+str(sub_user.id)+'/', data={'username': 'test2', 'fist_name': 'test2', 'last_name': 'testian2'}, format='json')
        self.assertEqual(r_users_change.status_code,
                         403)

    def test_can_edit_profile(self):
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)

            r_edit_profile = self.client.patch(
                '/api/users/EditProfile', data={'username': 'test2', 'fist_name': 'test22', 'last_name': 'testian2'}, format='json')
            self.assertEqual(r_edit_profile.status_code, 200)
