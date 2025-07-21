# places/forms.py
from django import forms
from .models import Establishment

class SightingForm(forms.Form):
    # Usamos um CharField para o produto, pois ele pode ser um produto novo.
    product_name = forms.CharField(
        label="Nome do Produto",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # Para o estabelecimento, um ModelChoiceField para selecionar da lista.
    establishment = forms.IntegerField(widget=forms.HiddenInput())