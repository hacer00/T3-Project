from django.contrib import admin
from .models import Announcements

@admin.register(Announcements)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')