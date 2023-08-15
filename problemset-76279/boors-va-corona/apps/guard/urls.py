from django.urls import path

from . import views

app_name = 'guard'

urlpatterns = [
    path('info', view=views.IpInfoAPIView.as_view(), name='client_info')
]
