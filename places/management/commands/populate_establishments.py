import googlemaps
from django.core.management.base import BaseCommand
from django.conf import settings
from places.models import Establishment, Product, ProductEstablishment

# Exemplo de como você poderia chamar uma IA.
# Você precisaria instalar uma biblioteca como a 'openai'.
# from openai import OpenAI

# Mock da função de IA para demonstração
def get_product_suggestions_from_ai(establishment_name, establishment_types):
    """
    Função FAKE que simula uma chamada de IA.
    Substitua pela sua implementação real.
    """
    print(f"IA: Gerando produtos para '{establishment_name}' do tipo '{establishment_types}'...")
    
    # Lógica de exemplo:
    if 'supermarket' in establishment_types or 'grocery_or_supermarket' in establishment_types:
        return ['Arroz', 'Feijão', 'Óleo de Soja', 'Açúcar', 'Café', 'Leite']
    if 'pharmacy' in establishment_types:
        return ['Analgésico', 'Antitérmico', 'Fraldas', 'Protetor Solar']
    if 'hardware_store' in establishment_types:
        return ['Martelo', 'Parafusos', 'Tinta', 'Cimento']
        
    return ['Coca-Cola', 'Água Mineral'] # Produtos genéricos

class Command(BaseCommand):
    help = 'Busca estabelecimentos no Google Places API e os popula no banco de dados'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando rotina de população de estabelecimentos...")
        gmaps = googlemaps.Client(key=settings.MAPS_API_KEY)
        
        # Em vez de 'places_nearby', 'text_search' pode ser mais abrangente
        # para buscar por tipos de estabelecimentos em uma cidade inteira.
        query = "supermercados em Ariquemes, RO" # Exemplo, você pode fazer várias buscas
        
        try:
            places_result = gmaps.places(query=query, language='pt-BR')
            
            for place in places_result.get('results', []):
                place_id = place['place_id']
                name = place['name']
                location = place['geometry']['location']
                
                # Cria ou atualiza o estabelecimento
                establishment, created = Establishment.objects.update_or_create(
                    google_place_id=place_id,
                    defaults={
                        'name': name,
                        'address': place.get('formatted_address', ''),
                        'lat': location['lat'],
                        'lng': location['lng'],
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Estabelecimento criado: {name}'))
                else:
                    self.stdout.write(f'Estabelecimento atualizado: {name}')

                # --- Integração com IA ---
                suggested_products = get_product_suggestions_from_ai(name, place.get('types', []))

                for prod_name in suggested_products:
                    product, _ = Product.objects.get_or_create(name=prod_name)
                    ProductEstablishment.objects.get_or_create(
                        product=product,
                        establishment=establishment
                    )
                self.stdout.write(f' -> Produtos associados: {", ".join(suggested_products)}')


        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar dados do Google: {e}'))

        self.stdout.write(self.style.SUCCESS('Rotina finalizada.'))