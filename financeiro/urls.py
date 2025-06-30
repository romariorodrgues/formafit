"""
URLs para gestão financeira.
"""
from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    # Dashboard financeiro
    path('', views.dashboard_financeiro, name='dashboard'),
]
