# Generated by Django 4.0.6 on 2022-07-15 21:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_payment', models.BigIntegerField(default=0)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('delivery_date', models.DateTimeField(null=True)),
                ('debt', models.PositiveBigIntegerField(default=0)),
                ('used_credit', models.PositiveBigIntegerField(default=0)),
                ('code', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_bills', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='bills.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('inventory', models.IntegerField(default=0)),
                ('discount', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('warranty', models.IntegerField(default=0)),
                ('price', models.BigIntegerField()),
                ('last_price', models.BigIntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='bills.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='BillProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sells', to='bills.bill')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sells', to='bills.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sells', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]