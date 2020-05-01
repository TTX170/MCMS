# Generated by Django 2.2.10 on 2020-04-22 07:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0011_auto_20200422_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtable',
            name='submissionFname',
            field=models.CharField(default='test', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subtable',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]