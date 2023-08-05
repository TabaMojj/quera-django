import re
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_national_code(self):
        data = self.cleaned_data
        national_code = data['national_code']
        if len(national_code) != 10:
            raise ValidationError('National Code must be 10 characters.')
        return national_code

    def clean_full_name(self):
        data = self.cleaned_data
        fullname = data['full_name']
        fullname_regex = re.compile(r'^[A-Z][a-zA-Z]{3,} [A-Z][a-zA-Z]{3,}$')
        if fullname_regex.match(fullname) is None:
            raise ValidationError('Full name is not correct.')
        return fullname
