from django.contrib import admin
from .models import Task ,TaskAttachment, TaskComment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'created_at')
    search_fields = ('title', 'description')

@admin.register(TaskAttachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'file', 'uploaded_at')
    search_fields = ('task__title',)

@admin.register(TaskComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    search_fields = ('task__title', 'user__username')