# Generated by Django 4.2.1 on 2023-07-13 04:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_membershippayment_pool_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershippayment',
            name='start_date',
            field=models.DateField(default=datetime.date(2023, 7, 13), verbose_name='Start date of the payment period'),
        ),
    ]
