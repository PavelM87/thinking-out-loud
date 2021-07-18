from django.urls import path

from .views import user_follow

urlpatterns = [
    path('<str:username>/follow', user_follow),
]
