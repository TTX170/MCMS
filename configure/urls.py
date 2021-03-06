from django.urls import path

from . import views

urlpatterns = [
    path('Tools', views.apicheck, name='apicheck'),
    path('', views.home, name='confhome'),
    path('BulkChange', views.bulkchange, name='bulkchange'),
    path('Backup', views.backup, name='backup'),
    path('Profile', views.profile, name='profile'),
]