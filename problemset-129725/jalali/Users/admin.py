from .forms import CustomUserForm
from .models import CustomUser
from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    @admin.display(description='first name')
    def first_name(self, obj):
        return obj.full_name.split()[0]

    @admin.display(description='last name')
    def last_name(self, obj):
        return obj.full_name.split()[1]

    form = CustomUserForm
    list_display = ['username', 'first_name', 'last_name', 'gender', 'national_code', 'birthday_date']
    search_fields = ['username', 'full_name']
    ordering = ['ceremony_datetime']