from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Announcements
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def announcement_list(request):
    announcements = Announcements.objects.order_by('-created_at')
    return render(request, 'announcements/list.html', {'announcements': announcements})

def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcements, pk=pk)
    return render(request, 'announcements/detail.html', {'announcement': announcement})


@login_required
def add_announcement(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Bu işlemi yapma yetkiniz yok.")
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        if title and content:
            Announcements.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, "Duyuru başarıyla eklendi!")
            return redirect("announcement_list") 

        messages.error(request, "Tüm alanları doldurun!")
    
    return render(request, "announcements/add_announcements.html")
