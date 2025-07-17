# places/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página HTML
    path('', views.search_page, name='search_page'),

    # --- NOVA ROTA PARA A API ---
    # Rota para devolver os dados dos locais em JSON
]