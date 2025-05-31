from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm,CustomUserChangeForm,TeamForm
from .models import CustomUser,Team
from django.db.models import Q
from django.urls import reverse
from tasks.models import Notification
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

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = request.user.notifications.filter(read=False).count()

    context = {
        'unread_notifications_count': unread_notifications_count
    }
    return render(request, "accounts/home.html", context)

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

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, current_user=request.user)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            form.save_m2m()
            team.members.add(request.user)

           #Takımı oluşturan kişiye bilgi
            Notification.objects.create(
                recipient=request.user,
                actor=request.user,
                verb=",Bir ekip oluşturdu",
                target=team.name,
                url=reverse('team_list')  
            )

            #Diğer üyelere bilgi
            for member in team.members.exclude(id=request.user.id):
                Notification.objects.create(
                    recipient=member,
                    actor=request.user,
                    verb=", Sizi ekibe ekledi",
                    target=team.name,
                    url=reverse('team_list')
                )

            messages.success(request, "Ekip başarıyla oluşturuldu.")
            return redirect('team_list')
    else:
        form = TeamForm(current_user=request.user)
    return render(request, 'accounts/create_team.html', {'form': form})

@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user == team.created_by:
        messages.error(request, "Bir ekip yöneticisi kendi oluşturduğu ekipten ayrılamaz.")
    elif request.user in team.members.all():
        team.members.remove(request.user)
        messages.success(request, f"{team.name} adlı ekipten ayrıldınız.")
    else:
        messages.warning(request, "Bu ekibin üyesi değilsiniz.")

    return redirect('team_list')

@login_required
def team_list(request):
    user = request.user
    teams = Team.objects.filter(Q(created_by=user) | Q(members=user)).distinct()
    return render(request, 'accounts/team_list.html', {'teams': teams})