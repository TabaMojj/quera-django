from django.urls import path

from . import views

app_name = 'market'

urlpatterns = [
    path('index', view=views.IndexAPIView.as_view(), name='index')
]
