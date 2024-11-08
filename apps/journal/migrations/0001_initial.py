# Generated by Django 4.2.1 on 2023-05-26 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pool', '0001_initial'),
        ('accounts', '0001_initial'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('entry_time', models.TimeField(auto_now_add=True, verbose_name='Entry time')),
                ('exit_time', models.TimeField(blank=True, null=True, verbose_name='Exit time')),
                ('actual_exit_time', models.TimeField(blank=True, null=True, verbose_name='Actual exit time')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create date')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='pool.key', verbose_name='Key')),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='accounts.membership', verbose_name='Membership')),
                ('membership_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='payments.paymenttype', verbose_name='Membership type')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='accounts.trainer', verbose_name='Trainer')),
            ],
            options={
                'verbose_name': 'Journal',
                'verbose_name_plural': 'Journals',
            },
        ),
    ]
