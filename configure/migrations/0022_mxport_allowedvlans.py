# Generated by Django 2.2.12 on 2020-04-25 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0021_mxport_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='mxport',
            name='allowedvlans',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]