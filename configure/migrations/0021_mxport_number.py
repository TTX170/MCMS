# Generated by Django 2.2.12 on 2020-04-24 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0020_auto_20200424_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='mxport',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
