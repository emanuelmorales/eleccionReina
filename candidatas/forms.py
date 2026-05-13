from django import forms
from .models import Candidata, Foto

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class FotoForm(forms.Form):
    fotos_subidas = forms.FileField(
        widget=MultipleFileInput(attrs={'class': 'file-input', 'multiple': True}),
        label="Seleccionar Fotos",
        required=False
    )
    descripcion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Descripción (opcional, se aplicará a todas)'}),
        label="Descripción"
    )

class CandidataForm(forms.ModelForm):
    class Meta:
        model = Candidata
        fields = ['nombre', 'apellido', 'dni', 'edad', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'text-input'}),
            'apellido': forms.TextInput(attrs={'class': 'text-input'}),
            'dni': forms.TextInput(attrs={'class': 'text-input'}),
            'edad': forms.NumberInput(attrs={'class': 'text-input'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'file-input'}),
        }
