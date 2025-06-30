"""
URL configuration for FormaFit project.
Sistema completo para personal trainers.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_dashboard(request):
    """Redireciona para o dashboard."""
    return redirect('accounts:dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard, name='home'),
    
    # Apps URLs
    path('auth/', include('accounts.urls')),
    path('alunos/', include('alunos.urls')),
    path('treinos/', include('treinos.urls')),
    path('frequencia/', include('frequencia.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('relatorios/', include('relatorios.urls')),
    # path('notificacoes/', include('notificacoes.urls')),
]

# Servir arquivos estáticos e media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
