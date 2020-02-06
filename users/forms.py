from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MerakiUser

class MerakiUserCreationForm(UserCreationForm):

    class Meta:
        model = MerakiUser
        fields = ('username','email','apikey')

class MerakiUserChangeForm(UserChangeForm):

    class Meta:
        model = MerakiUser
        fields = ('username', 'email','apikey')