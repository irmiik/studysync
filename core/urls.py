from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='rooms'),
    path('create-room/', views.create_room, name='create-room'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),
    path('room/<int:pk>/', views.room_detail, name='room-detail'),
    path('save-notes/<int:pk>/', views.save_notes, name='save-notes'),
]