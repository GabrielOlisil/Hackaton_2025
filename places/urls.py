# places/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página HTML
    path('', views.home_page, name='home_page'),
    path('buscar/', views.search_page, name='search_page'),
    path('add_sighting/', views.add_sighting, name='add_sighting'),
    path('like_sighting/<int:sighting_id>/', views.like_sighting, name='like_sighting'),
    path('api/search-establishments/', views.establishment_autocomplete, name='establishment_autocomplete'),
    path('product/<int:product_id>/locations/', views.product_locations, name='product_locations'),
    path('api/search-products/', views.product_autocomplete, name='product_autocomplete'),
]