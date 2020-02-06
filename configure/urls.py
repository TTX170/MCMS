from django.urls import path

from . import views

urlpatterns = [
    path('Tools', views.apicheck, name='apicheck'),
    path('', views.home, name='confhome'),
   # path('BulkChange', views.bulk, name='bulk'),
]