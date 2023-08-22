from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username',)


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username',)
