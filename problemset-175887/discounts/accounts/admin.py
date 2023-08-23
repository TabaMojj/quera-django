from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .forms import UserCreationForm, UserChangeForm

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            'Custom Field',  # you can also use None
            {
                'fields': (
                    'country',
                    'wallet',
                ),
            },
        ),
    )
