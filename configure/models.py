from django.db import models

# Create your models here.

class API(models.Model):
    apikey = models.CharField(max_length=200)
    orglist = models.CharField(max_length=200)
    networklist = models.CharField(max_length=200)
    permisson = models.CharField(max_length=200)
