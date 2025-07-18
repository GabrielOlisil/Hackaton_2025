from django.db import models

# Create your models here.
class Establishment(models.Model):
    google_place_id = models.CharField(max_length=255, unique=True, help_text="ID do lugar no Google Places")
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, null=True, blank=True, help_text="Endereço do estabelecimento")
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # Você pode adicionar um campo de categoria se desejar
    # category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductEstablishment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE)

    class Meta:
        # Garante que cada produto só seja associado uma vez a um estabelecimento
        unique_together = ('product', 'establishment')

    def __str__(self):
        return f"{self.product.name} @ {self.establishment.name}"