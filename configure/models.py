from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
import datetime
from encrypted_model_fields.fields import EncryptedCharField
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
    submissionID = models.ForeignKey("subtable", on_delete=models.CASCADE)
    
class vlan(models.Model):
    submissionID = models.ForeignKey("subtable", on_delete=models.CASCADE)
    netname = models.CharField(max_length=40)
    vlan = models.CharField(max_length=200)
    vlanname = models.CharField(max_length=200)
    mxip = models.CharField(max_length=200)
    subnet = models.CharField(max_length=200)
    dhcpstatus = models.CharField(max_length=200,blank = True,null=True)
    dhcprelayservers = models.CharField(max_length=200,blank = True,null=True)
    
class mxport(models.Model):
    submissionID = models.ForeignKey("subtable", on_delete=models.CASCADE)
    netname = models.CharField(max_length=40)
    enabled = models.CharField(max_length=10)
    porttype = models.CharField(max_length=200,blank = True,null=True)
    dropuntag = models.CharField(max_length=200,blank = True,null=True)
    vlan = models.CharField(max_length=200,blank = True,null=True)
    
class switch(models.Model):
    submissionID = models.ForeignKey("subtable", on_delete=models.CASCADE)
    serial = models.CharField(max_length=10)
    netname = models.CharField(max_length=40)
    enabled = models.CharField(max_length=10)
    portname = models.CharField(max_length=200,blank = True,null=True)
    porttype = models.CharField(max_length=200,blank = True,null=True)
    voicevlan = models.CharField(max_length=200,blank = True,null=True)
    vlan = models.CharField(max_length=200,blank = True,null=True)
    poe = models.CharField(max_length=200,blank = True,null=True)
    stp = models.CharField(max_length=200,blank = True,null=True)
    rstp = models.CharField(max_length=200,blank = True,null=True)
    

class subtable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    submissionFname = models.CharField(max_length=20) 
    date = models.DateTimeField(default=timezone.now)
    subtype = models.CharField(max_length=10,
        choices=(
            ("addDev", "addDev"),
            ("backupDev", "backupDev"),
            ("vlan", "vlan"),
            ("switch", "switch"),
            ("mxPort", "mxPort")
        )
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
        

class userprofile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="requester")
    apikey = EncryptedCharField(max_length=100)