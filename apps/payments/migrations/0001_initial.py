# Generated by Django 4.2.1 on 2023-05-26 13:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('type', models.CharField(choices=[('ONE_TIME', 'One-time entry'), ('WEEK', 'Weekly membership'), ('MONTH', 'Monthly membership'), ('QUARTER', 'Quarterly membership'), ('YEAR', 'Year membership'), ('CUSTOM', 'Custom membership')], default='MONTH', max_length=100, verbose_name='Memreship Type')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Price')),
                ('period', models.PositiveIntegerField(blank=True, null=True, verbose_name='Period')),
                ('visits_count', models.PositiveIntegerField(blank=True, null=True, verbose_name='Visits Count')),
                ('with_trainer', models.BooleanField(blank=True, default=False, null=True, verbose_name='With Trainer')),
                ('pool_duration', models.TimeField(blank=True, null=True, verbose_name='Pool Duration')),
            ],
            options={
                'verbose_name': 'Membership Type',
                'verbose_name_plural': 'Membership Types',
            },
        ),
        migrations.CreateModel(
            name='MembershipPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='Payment amount')),
                ('period', models.PositiveIntegerField(blank=True, null=True, verbose_name='Period')),
                ('visits_count', models.PositiveIntegerField(blank=True, null=True, verbose_name='Visits count')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='Start date of the payment period')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date of payment period')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('pool_duration', models.TimeField(blank=True, null=True, verbose_name='Pool duration')),
                ('is_active', models.BooleanField(blank=True, null=True, verbose_name='Is active')),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='accounts.membership', verbose_name='Membership')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainer', to='accounts.trainer', verbose_name='Trainer')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='payments.paymenttype', verbose_name='Membership Type')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
