"""
Views para gestão financeira.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

@login_required
def dashboard_financeiro(request):
    """
    Dashboard financeiro básico.
    """
    context = {
        'title': 'Dashboard Financeiro'
    }
    return render(request, 'financeiro/dashboard.html', context)
