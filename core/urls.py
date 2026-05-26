from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # register uses the path created in core/views.py. LoginView and LogoutView are built-in Django views for handling user authentication.
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), 
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]