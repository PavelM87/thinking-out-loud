from django.urls import path

from .views import (
    post_detail, post_list,
    post_create, post_delete, post_action
)

urlpatterns = [
    path('', post_list),
    path('action/', post_action),
    path('create/', post_create),
    path('<int:post_id>/', post_detail),
    path('<int:post_id>/delete/', post_delete),
]
