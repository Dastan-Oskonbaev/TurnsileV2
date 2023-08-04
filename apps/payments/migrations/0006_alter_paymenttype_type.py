# Generated by Django 4.2.1 on 2023-07-14 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_membershippayment_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttype',
            name='type',
            field=models.CharField(choices=[('ONE_TIME', 'One-time entry'), ('MEMBERSHIP', 'Membership')], default='MEMBERSHIP', max_length=100, verbose_name='Memreship Type'),
        ),
    ]