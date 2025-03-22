from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login,name="login"),
    path('register/', views.register,name="register"),
    path('home/',views.home,name="home"),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:pk>/edit/', views.post_update, name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
]
