import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from ..models import Profile


ALLOWED_HOSTS = settings.ALLOWED_HOSTS
User = get_user_model()


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_profile_detail(request, username, *args, **kwargs):
#     current_user = redirect.user
#     to_follow_user = 
#     return Response({}, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_follow(request, username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username=username)
    if not other_user_qs.exists():
        return Response({}, status=404)
    other = other_user_qs.first()
    profile = other.profile
    data = request.data or {}
    action = data.get("action")
    if action == "follow":
        profile.followers.add(me)
    elif action == "unfollow":
        profile.followers.remove(me)
    else:
        pass
    current_followers_qs = profile.followers.all()
    return Response({"count": current_followers_qs.count()}, status=200)
