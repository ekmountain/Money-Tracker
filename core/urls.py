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
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/create/', views.account_create, name='account_create'),
    path('accounts/<int:pk>/edit/', views.account_edit, name='account_edit'),
    path('accounts/<int:pk>/delete/', views.account_delete, name='account_delete'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/edit/', views.budget_edit, name='budget_edit'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
]