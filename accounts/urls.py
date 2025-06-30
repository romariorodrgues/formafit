"""
URLs para autenticação e dashboard.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticação
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/teste/', views.PerfilTestView.as_view(), name='perfil_test'),
    path('configuracoes/', views.ConfiguracoesView.as_view(), name='configuracoes'),
    path('teste-rolagem/', views.TesteRolagemView.as_view(), name='teste_rolagem'),
]
