from django.urls import path

from .views import user_follow, profile_detail_api

urlpatterns = [
    path('<str:username>/', profile_detail_api),
    path('<str:username>/follow', user_follow),
]
