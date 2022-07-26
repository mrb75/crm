from django.db import models
import datetime
import jdatetime
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        'users.User', models.CASCADE, related_name='categories', null=True, blank=True)
    parent = models.ForeignKey(
        'self', models.CASCADE, related_name='child', null=True, blank=True)
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


class Product(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        'users.User', models.CASCADE, related_name='products', blank=True, null=True)
    inventory = models.IntegerField(default=0)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    warranty = models.IntegerField(default=0)
    price = models.BigIntegerField()
    last_price = models.BigIntegerField()
    category = models.ForeignKey(
        Category, models.CASCADE, related_name='products')
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


class Bill(models.Model):
    user = models.ForeignKey(
        'users.User', models.CASCADE, related_name='personal_bills')
    cash_payment = models.BigIntegerField(default=0)
    description = models.TextField(max_length=1000, null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    debt = models.PositiveBigIntegerField(default=0)
    used_credit = models.PositiveBigIntegerField(default=0)
    code = models.CharField(max_length=100)
    creator = models.ForeignKey(
        'users.User', models.CASCADE, related_name='bills')
    products = models.ManyToManyField('Product', through='BillProduct')
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

    @property
    def delivery_date_time(self):
        return datetime.datetime.strftime(self.delivery_date, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.delivery_date).strftime('%Y/%m/%d %H:%M'))


class BillProduct(models.Model):
    seller = models.ForeignKey(
        'users.User', models.CASCADE, related_name='sells')
    bill = models.ForeignKey('Bill', models.CASCADE, related_name='sells')
    product = models.ForeignKey(
        'Product', models.CASCADE, related_name='sells')
    number = models.IntegerField(default=1)
