from django.contrib import admin

# Register your models here.
from .models import bulk,subtable,vlan,mxport,switch,userprofile

admin.site.register(bulk)
admin.site.register(subtable)
admin.site.register(vlan)
admin.site.register(mxport)
admin.site.register(switch)
admin.site.register(userprofile)