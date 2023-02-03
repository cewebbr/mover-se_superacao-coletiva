from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import UserChangeForm

from .forms import UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        (
            "Informações Pessoais", {
                "fields": (
                    "profile_picture",
                    "phone_number",
                    "cell_phone_number",
                    "zip",
                    "city",
                    "state",
                    "country",
                    "address",
                )
            },
        ),
    )
