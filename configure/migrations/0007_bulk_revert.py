# Generated by Django 2.2.10 on 2020-04-07 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0006_bulk_submissionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulk',
            name='revert',
            field=models.BooleanField(default=False),
        ),
    ]
