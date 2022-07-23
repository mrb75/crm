from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User, UserImage, Ticket
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
                             self.expected_status_users_change)

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

    def test_can_add_and_remove_image_for_own_sub_user(self):
        self.__jwt_auth(self.u_admin)
        sub_user = self.u_end
        image = open('files/images/aicon.png', 'rb')
        r_user_image_add = self.client.post(
            '/api/users/usersImage/', data={'image': image, 'user': sub_user.id})
        self.assertEqual(r_user_image_add.status_code, 200)
        # print(r_user_image_add.data)
        r_user_image_remove = self.client.delete(
            '/api/users/usersImage/'+str(r_user_image_add.data['created_image']['id'])+'/')
        self.assertEqual(r_user_image_remove.status_code, 200)

    def test_cant_add_and_remove_image_for_own_sub_user(self):
        other_admin = User.objects.create(
            username='u_other_admin', password='Mrb76420')
        # create another admin user
        other_admin.groups.add(Group.objects.get(name='admin_user'))
        # consider first global u_end(sub user of first admin) as sub user
        sub_user = self.u_end
        # authenticate with new admin which created in this test
        self.__jwt_auth(other_admin)

        # test other admin can not add image for su user of u_admin
        with open('files/images/aicon.png', 'rb') as image:
            r_user_image_add = self.client.post(
                '/api/users/usersImage/', data={'image': image, 'user': sub_user.id})
        self.assertEqual(r_user_image_add.status_code, 403)

        # authenticate with u_admin
        self.__jwt_auth(self.u_admin)

        # add image for u_end
        with open('files/images/aicon.png', 'rb') as image:
            r_user_image_add = self.client.post(
                '/api/users/usersImage/', data={'image': image, 'user': sub_user.id})

        # test other admin can not remove u_end image
        self.__jwt_auth(other_admin)
        r_user_image_remove = self.client.delete(
            '/api/users/usersImage/'+str(r_user_image_add.data['created_image']['id'])+'/')
        self.assertEqual(r_user_image_remove.status_code, 403)

        # remove created image
        self.__jwt_auth(self.u_admin)
        self.client.delete(
            '/api/users/usersImage/'+str(r_user_image_add.data['created_image']['id'])+'/')

    def test_can_add_ticket(self):
        self.__jwt_auth(self.u_end)
        r_add_tickets = self.client.post('/api/users/tickets/', data={'message_type': 'Management',
                                                                      'status': 'Waiting',
                                                                      'subject': 'test',
                                                                      'user': self.u_end.id,
                                                                      'text': 'hello world!',
                                                                      }, format='json')
        self.assertEqual(r_add_tickets.status_code, 201)

    def test_can_saw_own_tickets(self):
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            r_tickets = self.client.get('/api/users/tickets/', format='json')
            self.assertEqual(r_tickets.status_code, 200)

    def test_can_saw_one_ticket_of_own(self):
        other_user = User.objects.create(
            username='u_other_user', password='Mrb76420')
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            own_ticket = Ticket.objects.create(
                subject='own_ticket', user=user, text='its my own', message_type='Support', status='Waiting')
            r_ticket_own = self.client.get(
                '/api/users/tickets/'+str(own_ticket.id)+'/', format='json')
            self.assertEqual(r_ticket_own.status_code, 200)
            # create another admin user
            other_user.groups.add(Group.objects.get(name='end_user'))
            other_user_ticket = Ticket.objects.create(
                subject='own_ticket', user=other_user, text='its my own', message_type='Support', status='Waiting')
            r_ticket_other = self.client.get(
                '/api/users/tickets/'+str(other_user_ticket.id)+'/', format='json')
            self.assertEqual(r_ticket_other.status_code, 403)
