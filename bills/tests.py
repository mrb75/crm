from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Bill


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

    def test_saw_sub_users_bills(self):
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            r_bills = self.client.get('/api/bills/bills/', format='json')
            expected_status = 200 if user.has_perm('bills.view_bill') else 403
            self.assertEqual(r_bills.status_code, expected_status)

    def test_can_saw_single_bill(self):
        other_user = User.objects.create(
            username='u_other_user', password='Mrb76420')
        other_user.groups.add(Group.objects.get(name='end_user'))
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            other_user.admin = user
            other_user.save()
            bill = Bill.objects.create(
                cash_payment=1000, code='test', user=other_user, creator=user)
            r_bill = self.client.get(
                '/api/bills/bills/'+str(bill.id)+'/', format='json')
            expected_status = 200 if user.has_perm('bills.view_bill') else 403
            self.assertEqual(r_bill.status_code, expected_status)

    def test_cant_saw_single_bill(self):
        other_admin = User.objects.create(
            username='u_other_admin', password='Mrb76420')

        other_admin.groups.add(Group.objects.get(name='admin_user'))
        other_user = User.objects.create(
            username='u_other_user', password='Mrb76420', admin=other_admin)
        other_user.groups.add(Group.objects.get(name='end_user'))
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            bill = Bill.objects.create(
                cash_payment=1000, code='test', user=other_user, creator=user)
            r_bill = self.client.get(
                '/api/bills/bills/'+str(bill.id)+'/', format='json')
            self.assertEqual(r_bill.status_code, 403)

    def test_can_add_bill(self):
        for user in [self.u_admin, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            bill = Bill.objects.create(
                cash_payment=1000, code='test', user=other_user, creator=user)
            r_bill_add = self.client.post(
                '/api/bills/bills/', data={'cash_payment': 1000}, format='json')
            self.assertEqual(r_bill.status_code, 403)
