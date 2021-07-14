from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout


def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context ={
        "form": form,
        "btn_label": "Авторизация",
        "title": "Авторизация",
    }
    return render(request, "accounts/auth.html", context)

def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context ={
        "form": None,
        "description": "Хотите выйти из учетной записи?",
        "btn_label": "Подтвердите выход",
        "title": "Выход",
    }
    return render(request, "accounts/auth.html", context)

def registration_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
    context ={
        "form": form,
        "btn_label": "Регистрация",
        "title": "Регистрация",
    }
    return render(request, "accounts/auth.html", context)
