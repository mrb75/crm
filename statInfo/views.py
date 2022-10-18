from django.shortcuts import render
from rest_framework.views import APIView
from users.models import User
from bills.models import Bill
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models.aggregates import Count
from datetime import date


class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def __get_users_per_months_count(self, admin, months=1, is_bill=False):
        users = User.objects.filter(admin=admin)
        if is_bill:
            users = users.annotate(num_personal_bills=Count(
                'personal_bills')).filter(num_personal_bills__gt=0)
        for i in range(1, months+1):
            lower_time = timezone.now()-timedelta(days=30*(i))
            higher_time = timezone.now()-timedelta(days=30*(i-1))
            yield users.filter(date_joined__gte=lower_time, date_joined__lte=higher_time).count()

    def get(self, request, name):
        if not(request.user.has_perm('users.view_user')):
            return Response(403)
        if name == 'per_month_created_user':
            return Response([item for item in self.__get_users_per_months_count(request.user, 12)])
        elif name == 'per_month_users_has_bill':
            return Response([item for item in self.__get_users_per_months_count(request.user, 12, True)])
        else:
            return Response(status=404)


class BillStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def __get_bills_per_months_count(self, admin, year=0, months=1):
        bills = Bill.objects.filter(user__admin=admin)
        base_year = timezone.datetime.today().year if not(year) else year
        year_dif = timezone.datetime.today().year - base_year
        for i in range(1, months+1):
            lower_time = timezone.now()-timedelta(days=30*(i)) - \
                timedelta(days=365*year_dif)
            higher_time = timezone.now()-timedelta(days=30*(i-1)) - \
                timedelta(days=365*year_dif)
            yield bills.filter(date_created__gte=lower_time, date_created__lte=higher_time).count()

    def get(self, request, name):
        year = request.query_params['year'] if (
            'year' in request.query_params) else 0
        if not(request.user.has_perm('bills.view_bill')):
            return Response(403)
        if name == 'per_month_created_bill':
            return Response([item for item in self.__get_bills_per_months_count(request.user, int(year), 12)])
        else:
            return Response(status=404)
