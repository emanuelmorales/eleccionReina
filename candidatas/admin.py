from django.contrib import admin
from .models import Candidata, Foto

@admin.register(Candidata)
class CandidataAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'edad')
    search_fields = ('nombre', 'apellido', 'dni')

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('candidata', 'descripcion')
    list_filter = ('candidata',)
