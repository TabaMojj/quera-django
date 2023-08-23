from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path('login/', obtain_auth_token),
    path('upload/', UploadFile.as_view()),
    path('manager/', FileManager.as_view()),
    path('download/<str:user>/<str:filename>', DownloadFile.as_view())
]
