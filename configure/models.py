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
    name = models.CharField(max_length=200,blank = True,null=True)
    tags = models.CharField(max_length=200,blank = True,null=True)
    notes = models.CharField(max_length=200,blank = True,null=True)
    address = models.CharField(max_length=200,blank = True,null=True)
    ip = models.CharField(max_length=200,blank = True,null=True)
    gw = models.CharField(max_length=200,blank = True,null=True)
    mask = models.CharField(max_length=200,blank = True,null=True)
    dns1 = models.CharField(max_length=200,blank = True,null=True)
    dns2 = models.CharField(max_length=200,blank = True,null=True)
    vlan = models.CharField(max_length=200,blank = True,null=True)
    nettags = models.CharField(max_length=200,blank = True,null=True)
    owner = models.ForeignKey(MerakiUser, on_delete=models.CASCADE, related_name="requests")
    revert = models.BooleanField(default = False)
    submissionID = models.CharField(max_length=10)
    

