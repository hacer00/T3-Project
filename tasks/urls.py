from django.urls import path
from . import views

urlpatterns = [
    path('tasks_list/', views.task_list, name='task_list'),
    path('update-task-status/<int:task_id>/<str:new_status>/', views.update_task_status, name='update_task_status'),
    path('add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/add_comment/', views.add_comment, name='add_comment'),
    path('task/<int:task_id>/add_attachment/', views.add_attachment, name='add_attachment'),
    path('notifications/', views.notification_list, name='notification_list'),

]
