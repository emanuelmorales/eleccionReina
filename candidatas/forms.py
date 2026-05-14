from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .models import Candidata, Foto, Puntuacion

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class FotoForm(forms.Form):
    fotos_subidas = forms.FileField(
        widget=MultipleFileInput(attrs={'class': 'file-input', 'multiple': True}),
        label="Seleccionar Fotos",
        required=False,
        help_text="Recomendado: Fotos verticales 600x800px para la galeria. Se recortaran automaticamente. Formatos: JPG, PNG"
    )
    descripcion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Descripcion (opcional, se aplicara a todas)'}),
        label="Descripcion"
    )

class PuntuacionForm(forms.ModelForm):
    class Meta:
        model = Puntuacion
        fields = ['belleza', 'simpatia', 'elegancia', 'vestimenta', 'maquillaje', 'hinchada']
        widgets = {
            'belleza': forms.NumberInput(attrs={'class': 'score-input', 'min': '1', 'max': '10', 'placeholder': '1-10'}),
            'simpatia': forms.NumberInput(attrs={'class': 'score-input', 'min': '1', 'max': '10', 'placeholder': '1-10'}),
            'elegancia': forms.NumberInput(attrs={'class': 'score-input', 'min': '1', 'max': '10', 'placeholder': '1-10'}),
            'vestimenta': forms.NumberInput(attrs={'class': 'score-input', 'min': '1', 'max': '10', 'placeholder': '1-10'}),
            'maquillaje': forms.NumberInput(attrs={'class': 'score-input', 'min': '1', 'max': '10', 'placeholder': '1-10'}),
            'hinchada': forms.NumberInput(attrs={'class': 'score-input', 'min': '1', 'max': '10', 'placeholder': '1-10'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['belleza', 'simpatia', 'elegancia', 'vestimenta', 'maquillaje', 'hinchada']:
            self.fields[field].validators = [
                MinValueValidator(1),
                MaxValueValidator(10)
            ]

class CandidataForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'text-input', 'type': 'date'}),
        required=False,
        label='Fecha de Nacimiento'
    )
    turno = forms.ChoiceField(
        choices=Candidata.TURNO_CHOICES, 
        widget=forms.Select(attrs={'class': 'text-input'}), 
        required=False, 
        label='Turno'
    )
    
    class Meta:
        model = Candidata
        fields = ['nombre', 'apellido', 'dni', 'edad', 'fecha_nacimiento', 'curso', 'division', 'turno', 'especialidad', 'estatura', 'pasatiempos', 'proyectos_aspiraciones', 'imagen']
        labels = {
            'imagen': 'Foto de Perfil',
        }
        help_texts = {
            'imagen': 'Recomendado: Foto cuadrada 400x400px. Se recortara automaticamente si es necesario. Formatos: JPG, PNG',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.fecha_nacimiento:
            self.initial['fecha_nacimiento'] = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')
