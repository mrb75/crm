# Generated by Django 4.0.6 on 2022-07-23 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_rename_user_billproduct_customer_product_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='products',
            new_name='bills',
        ),
    ]