# Generated by Django 4.2.1 on 2023-05-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historytype',
            name='icon',
            field=models.URLField(verbose_name='Icon'),
        ),
    ]
