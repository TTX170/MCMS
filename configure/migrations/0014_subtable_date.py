# Generated by Django 2.2.10 on 2020-04-22 07:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0013_auto_20200422_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtable',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]