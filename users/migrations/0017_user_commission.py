# Generated by Django 4.0.6 on 2022-08-31 07:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_turn_user_alter_turn_coworker_alter_turn_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='commission',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
