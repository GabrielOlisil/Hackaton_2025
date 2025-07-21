# places/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Establishment, Product, ProductEstablishment
from django.contrib.postgres.search import SearchQuery, SearchVector
from .forms import SightingForm
from django.contrib.auth.decorators import login_required # Para proteger a view
from django.db import models
from django.http import JsonResponse
import json

def home_page(request):
    return redirect("buscar/")

def search_page(request):
    query = request.GET.get('q', None)
    products = Product.objects.none()

    if query:
        search_query = SearchQuery(query, config='portuguese')
        products = Product.objects.filter(search_vector=search_query)

    context = {
        'products': products,
        'query': query or ''
    }
    
    return render(request, 'places/search_page.html', context)

def product_locations(request, product_id):
    # Pega o produto específico ou retorna um erro 404
    product = get_object_or_404(Product, id=product_id)

    # Busca os "avistamentos" (locais) para este produto, ordenados por likes
    sightings = ProductEstablishment.objects.filter(
        product=product
    ).annotate(
        num_likes=models.Count('likes')
    ).order_by('-num_likes')

    # Prepara os dados para o mapa, como antes
    map_data = []
    for s in sightings:
        map_data.append({
            'lat': s.establishment.lat,
            'lng': s.establishment.lng,
            'name': s.establishment.name,
            'address': s.establishment.address,
            'likes': s.total_likes
        })

    context = {
        'product': product,
        'sightings': sightings,
        'map_data_json': json.dumps(map_data)
    }
    
    return render(request, 'places/product_locations.html', context)

@login_required # Garante que apenas usuários logados acessem esta página
def add_sighting(request):
    # Preenche o formulário com o nome do produto se ele veio da busca
    if request.method == 'POST':
        form = SightingForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            establishment_id = form.cleaned_data['establishment']

            try:
                establishment_obj = Establishment.objects.get(id=establishment_id)
            except Establishment.DoesNotExist:
                # Handle error if the establishment doesn't exist, though it shouldn't happen
                form.add_error('establishment', 'Estabelecimento inválido selecionado.')
                return render(request, 'places/add_sighting.html', {'form': form})
            

            # Usa update_or_create para criar o produto ou atualizar o existente.
            # Isso também garante que o search_vector seja populado.
            product, created = Product.objects.get_or_create(
                name__iexact=product_name,
                defaults={
                    'name': product_name,
                }
            )

            if created: 
                product.search_vector = SearchVector('name', config='portuguese')
                product.save()

            # Cria a ligação entre o produto e o estabelecimento
            sighting, created = ProductEstablishment.objects.get_or_create(
                product=product,
                establishment=establishment_obj,
                defaults={'created_by': request.user}
            )

            # Redireciona para a busca do produto recém-adicionado
            return redirect(f"/buscar/?q={product.name}")
    
    # Se não for POST, é um GET: exibe o formulário em branco ou com dados iniciais
    else:
        initial_data = {'product_name': request.GET.get('product_name')}
        form = SightingForm(initial=initial_data)

    # Renderiza a página com o formulário (seja ele em branco ou com erros de validação)
    return render(request, 'places/add_sighting.html', {'form': form})

@login_required
def like_sighting(request, sighting_id):
    # Pega o objeto do "avistamento" ou retorna um erro 404 se não existir
    sighting = get_object_or_404(ProductEstablishment, id=sighting_id)

    # Verifica se o usuário já deu like
    if sighting.likes.filter(id=request.user.id).exists():
        # Se já deu, remove o like (toggle)
        sighting.likes.remove(request.user)
    else:
        # Se não deu, adiciona o like
        sighting.likes.add(request.user)

    # Redireciona de volta para a busca do produto original
    return redirect(f"/product/{sighting.product.id}/locations/")


def establishment_autocomplete(request):
    query = request.GET.get('q', '')
    establishments = Establishment.objects.none()

    if len(query) > 2: # Só busca se o usuário digitou pelo menos 3 caracteres
        search_query = SearchQuery(query, config='portuguese')
        establishments = Establishment.objects.filter(search_vector=search_query)[:10] # Limita a 10 resultados

    # Transforma o resultado em uma lista de dicionários seguros para JSON
    results = [{'id': est.id, 'name': est.name} for est in establishments]

    return JsonResponse(results, safe=False)

def product_autocomplete(request):
    query = request.GET.get('q', '')
    products = Product.objects.none()

    # Só busca se o usuário digitou pelo menos 2 caracteres
    if len(query) > 1:
        search_query = SearchQuery(query, config='portuguese')
        # Busca no campo de busca textual e limita a 10 resultados
        products = Product.objects.filter(search_vector=search_query)[:10] 

    # Transforma o resultado em uma lista de nomes de produtos
    results = [p.name for p in products]

    return JsonResponse(results, safe=False)