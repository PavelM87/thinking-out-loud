import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from ..models import Post
from ..forms import PostForm
from ..serializers import PostSerializer, PostActionSerializer, PostCreateSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS



@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def post_create(request, *args, **kwargs):
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
       serializer.save(user=request.user)
       return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def post_detail(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_delete(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "Ты не можешь удалить этот пост"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Пост удален"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action(request, *args, **kwargs):
    '''
    Действия: Лайк, дизлайк, репост
    '''
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Post.objects.filter(id=post_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            print(request.user)
            obj.likes.add(request.user)
            serializer = PostSerializer(obj)            
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = PostSerializer(obj)            
            return Response(serializer.data, status=200)
        elif action == "repost":
            new_post = Post.objects.create(user=request.user, parent=obj, content=content)
            serializer = PostSerializer(new_post)
            return Response(serializer.data, status=201)
    return Response({}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_feed(request, *args, **kwargs):
    user = request.user
    qs = Post.objects.feed(user)
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def post_list(request, *args, **kwargs):
    qs = Post.objects.all()
    username = request.GET.get('username')
    if username != None:
        # qs = qs.filter(user__username__iexact=username)
        qs = qs.by_username(username)
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)

