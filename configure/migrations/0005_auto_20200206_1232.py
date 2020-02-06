# Generated by Django 2.2.10 on 2020-02-06 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0004_bulk_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulk',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
