# places/views.py

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse # Importe JsonResponse
import googlemaps

# A view que serve a página HTML (já existe)
def search_page(request):
    context = {}
    return render(request, 'places/search_page.html', context)

# --- NOVA VIEW PARA A API ---
def list_places_api(request):
    gmaps = googlemaps.Client(key=settings.MAPS_API_KEY)
    ariquemes_location = (-9.9133, -63.0410)

    try:
        places_result = gmaps.places_nearby(
            location=ariquemes_location,
            radius=5000,
            keyword='comércio',
            language='pt-BR'
        )
        
        places_list = []
        for place in places_result.get('results', []):
            places_list.append({
                'place_id': place['place_id'],
                'name': place.get('name'),
                'vicinity': place.get('vicinity'),
                'location': place.get('geometry', {}).get('location'),
                'rating': place.get('rating', 'N/A'),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'types': place.get('types', []) # <-- ADICIONAMOS ESTA LINHA
            })

        return JsonResponse({'places': places_list})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
