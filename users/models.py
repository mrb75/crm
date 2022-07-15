from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import jdatetime
from django.utils.translation import gettext as _


class Country(models.Model):
    name = models.CharField(max_length=30)
    phone_code = models.CharField(max_length=5)


class Province(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(
        Country, models.CASCADE, related_name='provinces')


class City(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(
        Province, models.CASCADE, related_name='cities')


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'Male', _('مرد')
        FEMALE = 'Female', _('زن')
        NOTHING = 'Nothing', _('هیچکدام')
    email = models.EmailField(unique=True, null=True)
    mobile = models.CharField(unique=True, null=True, max_length=10)
    birth_date = models.DateField(null=True)
    city = models.ForeignKey(City, models.CASCADE,
                             related_name='users', null=True)
    national_code = models.CharField(max_length=10, null=True)
    description = models.TextField(max_length=1000, null=True)
    gender = models.CharField(choices=Gender.choices,
                              default=Gender.NOTHING, max_length=10)
    credit = models.BigIntegerField(default=0)
    point = models.IntegerField(default=0)
    company_name = models.CharField(max_length=60, null=True)
    remained_sms = models.IntegerField(default=0)
    date_modified = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['is_staff', 'is_active', 'date_joined']

    class Meta:
        ordering = ['date_joined']

    @property
    def create_date_time(self):
        return datetime.datetime.strftime(self.date_joined, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_joined).strftime('%Y/%m/%d %H:%M'))

    @property
    def modify_date_time(self):
        return datetime.datetime.strftime(self.date_modified, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_modified).strftime('%Y/%m/%d %H:%M'))


class UserImage(models.Model):
    path = models.ImageField(upload_to='files/images')
    user = models.ForeignKey(User, models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']

    @property
    def create_date_time(self):
        return datetime.datetime.strftime(self.date_created, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_created).strftime('%Y/%m/%d %H:%M'))

    @property
    def modify_date_time(self):
        return datetime.datetime.strftime(self.date_modified, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_modified).strftime('%Y/%m/%d %H:%M'))
