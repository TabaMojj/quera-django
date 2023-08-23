from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RevokeTokenView

app_name = 'accounts'

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', RevokeTokenView.as_view(), name='logout'),
]
