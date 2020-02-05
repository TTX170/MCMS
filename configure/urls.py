from django.urls import path

from . import views

urlpatterns = [
    path('Tools', views.apicheck, name='apicheck'),
]