# places/views.py

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse # Importe JsonResponse
import googlemaps
import json 
# A view que serve a página HTML (já existe)
def search_page(request):
    gmaps = googlemaps.Client(key=settings.MAPS_API_KEY)
    ariquemes_location = (-9.9133, -63.0410)
    
    context = {
        'places': [],
        'places_json': '[]' # Valor padrão caso a busca falhe
    }

    try:
        places_result = gmaps.places_nearby(
            location=ariquemes_location,
            radius=5000,
            page_token='ATKogpcz_czOPjE06NeAqpLEAteQJl4p9zCE6TAFh1WALhugqFH0q5DNeWXoINh8ZigNAb91WWSmQ2dreQOCT5e0ZY5iR6FCr0lvOU4g1UhraaXo-sN4Jk2-_ocSmzBJjdleD1hHEEtp6AnVTS_xMMy9sTHUrqURXyoizaODQyHXyerQrbipScaiuZ1hWB43V5TN1QTC0739Dna3Ab21TETe9EYssTCpf8ZvJ7uO825u4S-s15piMOzX_RLsyJTfdqtqi_WrKVqGRBZpXqr35g7WpaKTvgA_wkjngxxidvYlNGJ1eWwWSlOsRpSrkRQpx7o0DkfZjtMhB9M5mtsQvQLl08_4m5XstcZJGtqVSCsadL_QapHJp0a9XiF0CKS_Lmtf2D5_ytAlQNopb68xg8h-igUr61_990WeWxsmPp2lSnjc',
            language='pt-BR'
        )
        print(f"DEBUG: Status da resposta do Google: {places_result}")

        places_list = []
        for place in places_result.get('results', []):
            places_list.append({
                'id': place.get('place_id', "Id"),
                'name': place.get('name', 'Nome não disponível'),
                'vicinity': place.get('vicinity', 'Endereço não disponível'),
                'location': place.get('geometry', {}).get('location'),
                'rating': place.get('rating', 'N/A'),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'types': place.get('types', [])
            })
        
        # Passa a lista para o contexto do template
        context['places'] = places_list
        # Passa a mesma lista em formato JSON para ser usada pelo JavaScript
        context['places_json'] = json.dumps(places_list)

    except Exception as e:
        # Em caso de erro, o contexto já tem valores padrão seguros
        print(f"Erro ao buscar locais na API do Google: {e}")

    return render(request, 'places/search_page.html', context)

