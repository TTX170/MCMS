from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import MerakiUserCreationForm, MerakiUserChangeForm
from .models import MerakiUser

class MerakiUserAdmin(UserAdmin):
    add_form = MerakiUserCreationForm
    form = MerakiUserChangeForm
    model = MerakiUser
    list_display = ['email', 'username','apikey']

admin.site.register(MerakiUser, MerakiUserAdmin)
