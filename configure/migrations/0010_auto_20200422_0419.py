# Generated by Django 2.2.10 on 2020-04-22 04:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configure', '0009_auto_20200408_0106'),
    ]

    operations = [
        migrations.CreateModel(
            name='subtable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subtype', models.CharField(choices=[(1, 'addDev'), (2, 'backupDev'), (3, 'vlan'), (4, 'switch'), (5, 'mxPort')], max_length=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='bulk',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='bulk',
            name='revert',
        ),
        migrations.AlterField(
            model_name='bulk',
            name='submissionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configure.subtable'),
        ),
        migrations.CreateModel(
            name='vlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('netname', models.CharField(max_length=40)),
                ('vlan', models.CharField(max_length=200)),
                ('vlanname', models.CharField(max_length=200)),
                ('mxip', models.CharField(max_length=200)),
                ('subnet', models.CharField(max_length=200)),
                ('dhcpstatus', models.CharField(blank=True, max_length=200, null=True)),
                ('dhcprelayservers', models.CharField(blank=True, max_length=200, null=True)),
                ('submissionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configure.subtable')),
            ],
        ),
        migrations.CreateModel(
            name='switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=10)),
                ('netname', models.CharField(max_length=40)),
                ('enabled', models.CharField(max_length=10)),
                ('portname', models.CharField(blank=True, max_length=200, null=True)),
                ('porttype', models.CharField(blank=True, max_length=200, null=True)),
                ('voicevlan', models.CharField(blank=True, max_length=200, null=True)),
                ('vlan', models.CharField(blank=True, max_length=200, null=True)),
                ('poe', models.CharField(blank=True, max_length=200, null=True)),
                ('stp', models.CharField(blank=True, max_length=200, null=True)),
                ('rstp', models.CharField(blank=True, max_length=200, null=True)),
                ('submissionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configure.subtable')),
            ],
        ),
        migrations.CreateModel(
            name='mxport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('netname', models.CharField(max_length=40)),
                ('enabled', models.CharField(max_length=10)),
                ('porttype', models.CharField(blank=True, max_length=200, null=True)),
                ('dropuntag', models.CharField(blank=True, max_length=200, null=True)),
                ('vlan', models.CharField(blank=True, max_length=200, null=True)),
                ('submissionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configure.subtable')),
            ],
        ),
    ]