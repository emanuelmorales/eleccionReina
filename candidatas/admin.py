from django.contrib import admin
from .models import Candidata, Foto, Puntuacion

@admin.register(Candidata)
class CandidataAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'curso', 'division', 'turno', 'especialidad')
    search_fields = ('nombre', 'apellido', 'dni', 'especialidad')
    list_filter = ('turno', 'curso', 'division')

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('candidata', 'descripcion')
    list_filter = ('candidata',)

@admin.register(Puntuacion)
class PuntuacionAdmin(admin.ModelAdmin):
    list_display = ('candidata', 'belleza', 'simpatia', 'elegancia', 'vestimenta', 'maquillaje', 'hinchada', 'total')
    list_filter = ('candidata',)
