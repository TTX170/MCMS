from django.db import models
from users.models import MerakiUser

# Create your models here.

class API(models.Model):
    apikey = models.CharField(max_length=200)
    orglist = models.CharField(max_length=200)
    networklist = models.CharField(max_length=200)
    permisson = models.CharField(max_length=200)

class bulk(models.Model):
    serial = models.CharField(max_length=200)
    networkname = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    gw = models.CharField(max_length=200)
    mask = models.CharField(max_length=200)
    dns1 = models.CharField(max_length=200)
    dns2 = models.CharField(max_length=200)
    vlan = models.CharField(max_length=200)
    nettags = models.CharField(max_length=200)
    owner = models.ForeignKey(MerakiUser, on_delete=models.CASCADE, related_name="requests")
    

