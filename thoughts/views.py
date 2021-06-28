from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Post


def home(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)

def post_detail(request, post_id, *args, **kwargs):

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
