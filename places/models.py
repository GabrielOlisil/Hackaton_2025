from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.conf import settings
from places.utils import remover_acentos

# Create your models here.
class Establishment(models.Model):
    google_place_id = models.CharField(max_length=255, unique=True, help_text="ID do lugar no Google Places")
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, null=True, blank=True, help_text="Endereço do estabelecimento")
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    search_vector = SearchVectorField(null=True, editable=False)
    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    # Campo que armazenará o texto otimizado para busca. Não será editável no admin.
    search_vector = SearchVectorField(null=True, editable=False)

    def __str__(self):
        return self.name
    

    class Meta:
        # Cria um índice GIN no campo search_vector, que é o tipo ideal para full-text search.
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

class ProductEstablishment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE)

    # CAMPOS NOVOS
    # Guarda quem fez a sugestão. Se o usuário for deletado, o campo fica nulo.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # Guarda a data e hora da criação
    created_at = models.DateTimeField(auto_now_add=True)


    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_sightings', # Nome para o relacionamento reverso
        blank=True
    )
    class Meta:
        unique_together = ('product', 'establishment')

    def __str__(self):
        return f"{self.product.name} @ {self.establishment.name}"
    
    @property
    def total_likes(self):
        return self.likes.count()