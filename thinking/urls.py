"""thinking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from thoughts.views import (
    home, post_detail, post_list,
    post_create, post_delete, post_action
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('create-post', post_create),
    path('posts', post_list),
    path('posts/<int:post_id>', post_detail),
    path('api/posts/', include('thoughts.urls')),
    # path('api/posts/action', post_action),
    # path('api/posts/<int:post_id>/delete', post_delete),
]
