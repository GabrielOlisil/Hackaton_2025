# places/views.py
from django.shortcuts import render
from .models import Establishment, Product, ProductEstablishment
import json

def search_page(request):
    query = request.GET.get('q', None) # Pega o parâmetro de busca 'q' da URL
    places_list = []

    if query:
        # 1. Busca no SEU banco de dados
        # Encontra produtos que contenham o texto da busca (insensível a maiúsculas)
        products = Product.objects.filter(name__icontains=query)
        
        # Encontra todos os estabelecimentos que vendem esses produtos
        establishments = Establishment.objects.filter(productestablishment__product__in=products).distinct()
        
        for est in establishments:
            places_list.append({
                'id': est.google_place_id,
                'name': est.name,
                'vicinity': est.address, # Usando o endereço do nosso banco
                'location': {'lat': est.lat, 'lng': est.lng},
            })
    
    context = {
        'places': places_list,
        'places_json': json.dumps(places_list),
        'query': query or ''
    }
    
    return render(request, 'places/search_page.html', context)