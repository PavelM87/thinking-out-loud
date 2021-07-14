from django.shortcuts import render


def profile_detail(request, username, *args, **kwargs):
    return render(request, "profiles/detail.html", {"username": username})