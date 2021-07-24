from django.urls import path

from .views import profile_detail_api

urlpatterns = [
    path('<str:username>/', profile_detail_api),
    path('<str:username>/follow', profile_detail_api),
]
