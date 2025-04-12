from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path("add/", views.add_announcement, name="add_announcement"),
]
