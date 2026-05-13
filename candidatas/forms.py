from django import forms
from django.utils.translation import gettext_lazy as _
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.fecha_nacimiento:
            self.initial['fecha_nacimiento'] = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')
