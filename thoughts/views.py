import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Post
from .forms import PostForm
from .serializers import PostSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)

@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def post_create(request, *args, **kwargs):
    serializer = PostSerializer(data=request.POST)
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

@api_view(['GET'])
def post_list(request, *args, **kwargs):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)

def post_create_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = PostForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = PostForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form': form})

def post_list_pure_django(request, *args, **kwargs):
    qs = Post.objects.all()
    posts_list = [x.serialize() for x in qs]
    data = {
        'isUser': False,
        'response': posts_list
    }
    return JsonResponse(data)

def post_detail_pure_django(request, post_id, *args, **kwargs):

    data = {
        "id": post_id,
    }
    status = 200
    try:
        obj = Post.objects.get(id=post_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)
