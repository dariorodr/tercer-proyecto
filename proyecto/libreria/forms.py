from django import forms
from .models import ProductoTemporada, Receta

class ProductoTemporadaForm(forms.ModelForm):
    class Meta:
        model = ProductoTemporada
        fields = '__all__'

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = '__all__'
        
        