# Generated by Django 2.2.10 on 2020-04-08 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0008_auto_20200408_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulk',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='dns1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='dns2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='gw',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='ip',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='mask',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='nettags',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='notes',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='tags',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bulk',
            name='vlan',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
