from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser

def register(request): #kayıt olma
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request): #giris yapma
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı!")
    return render(request, "accounts/login.html")

def home(request): #anasayfa
    return render(request,"accounts/home.html")

def post_list(request): #girislerin listelenmesi
    posts = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/post_list.html', {'posts': posts})

def post_update(request, pk): #girislerin güncellenebilmesi
    post = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list') 
    else:
        form = CustomUserChangeForm(instance=post)
    return render(request, 'accounts/post_update.html', {'form': form})

def post_delete(request, pk): #girislerin silinmesi
    post = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'accounts/post_confirm_delete.html', {'post': post})