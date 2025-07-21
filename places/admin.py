# places/admin.py

from django.contrib import admin
from .models import Product, Establishment, ProductEstablishment

# --- Configuração da Administração para ProductEstablishment ---

@admin.register(ProductEstablishment)
class ProductEstablishmentAdmin(admin.ModelAdmin):
    """
    Personaliza a forma como os "avistamentos" (ligações produto-comércio)
    são exibidos na área administrativa.
    """
    # Define as colunas que aparecerão na lista de avistamentos
    list_display = (
        'product',
        'establishment',
        'created_by',
        'created_at',
        'total_likes',
    )

    # Adiciona filtros na barra lateral direita para facilitar a navegação
    list_filter = (
        'created_at',
        'establishment',
    )

    # Adiciona um campo de busca
    search_fields = (
        'product__name',
        'establishment__name',
        'created_by__username',
    )

    # Ordenação padrão: os mais recentes primeiro
    ordering = ('-created_at',)

    # Ações personalizadas que podem ser executadas em lote
    actions = ['delete_selected']

    # Desativa a permissão de adicionar/mudar avistamentos manualmente pelo admin,
    # pois isso deve vir da contribuição do usuário.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# --- Registros Simples para os Outros Modelos ---

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuração básica para administrar Produtos.
    """
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    """
    Configuração básica para administrar Estabelecimentos.
    """
    list_display = ('name', 'address')
    search_fields = ('name',)
