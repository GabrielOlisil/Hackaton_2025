import time
import googlemaps
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from places.models import Establishment

class Command(BaseCommand):
    help = 'Busca exaustivamente por todos os tipos de estabelecimentos em Ariquemes e os popula no banco de dados.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- INICIANDO ROTINA DE CENSO DE ESTABELECIMENTOS ---'))
        gmaps = googlemaps.Client(key=settings.MAPS_API_KEY)

        # Coordenadas do centro de Ariquemes, RO
        location = (-9.9133, -63.0411)
        # Um raio grande para cobrir a área urbana
        radius = 5000  # 5 km

        # Lista exaustiva de tipos de lugares que a API do Google reconhece.
        # Isso garante a maior cobertura possível.
        place_types = [
            'art_gallery', 'bakery', 'bar', 'bicycle_store', 'book_store',
            'car_dealer', 'clothing_store', 'convenience_store',
            'department_store', 'drugstore', 'electronics_store', 'florist',
            'furniture_store', 'gas_station', 'hardware_store',
            'home_goods_store', 'jewelry_store', 'liquor_store',
            'meal_delivery', 'meal_takeaway', 'movie_rental', 'night_club',
            'pet_store', 'pharmacy', 'restaurant', 'shoe_store',
            'shopping_mall', 'store', 'supermarket'
        ]

        # Um set para guardar os place_id's já processados e evitar duplicatas
        processed_place_ids = set()
        total_new_establishments = 0

        for place_type in place_types:
            self.stdout.write(self.style.HTTP_INFO(f'\nBuscando por categoria: "{place_type}"...'))
            
            try:
                # Faz a primeira busca para a categoria
                response = gmaps.places_nearby(location=location, radius=radius, type=place_type, language='pt-BR')
                
                while True:
                    # Processa os resultados da página atual
                    for place in response.get('results', []):
                        place_id = place['place_id']
                        if place_id in processed_place_ids:
                            continue # Pula se já processamos este lugar

                        processed_place_ids.add(place_id)
                        
                        establishment, created = Establishment.objects.update_or_create(
                            google_place_id=place_id,
                            defaults={
                                'name': place['name'],
                                'address': place.get('vicinity', ''),
                                'lat': place['geometry']['location']['lat'],
                                'lng': place['geometry']['location']['lng'],
                            }
                        )

                        # Atualiza o search_vector para a busca textual
                        establishment.search_vector = SearchVector('name', config='portuguese')
                        establishment.save()

                        if created:
                            total_new_establishments += 1
                            self.stdout.write(f'  -> NOVO: {place["name"]}')

                    # Lógica de Paginação: verifica se há uma próxima página
                    next_page_token = response.get('next_page_token')
                    if next_page_token:
                        self.stdout.write(self.style.SUCCESS('  ...encontrada próxima página, aguardando 2 segundos...'))
                        # A API exige uma pequena pausa antes de usar o token
                        time.sleep(2)
                        response = gmaps.places_nearby(page_token=next_page_token)
                    else:
                        # Se não há mais páginas, quebra o loop e vai para a próxima categoria
                        break
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Erro ao buscar categoria "{place_type}": {e}'))

        self.stdout.write(self.style.SUCCESS(f'\n--- ROTINA FINALIZADA ---'))
        self.stdout.write(self.style.SUCCESS(f'Total de estabelecimentos únicos processados: {len(processed_place_ids)}'))
        self.stdout.write(self.style.SUCCESS(f'Total de novos estabelecimentos adicionados nesta rotina: {total_new_establishments}'))