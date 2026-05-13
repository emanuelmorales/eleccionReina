from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_candidatas, name='lista_candidatas'),
    path('candidata/<int:pk>/', views.detalle_candidata, name='detalle_candidata'),
    path('candidata/<int:pk>/subir-foto/', views.subir_foto, name='subir_foto'),
    path('candidata/agregar/', views.agregar_candidata, name='agregar_candidata'),
    path('candidata/<int:pk>/editar/', views.editar_candidata, name='editar_candidata'),
    path('candidata/<int:pk>/eliminar/', views.eliminar_candidata, name='eliminar_candidata'),
    path('candidata/<int:pk>/puntuar/', views.puntuar_candidata, name='puntuar_candidata'),
    path('foto/<int:pk>/eliminar/', views.eliminar_foto, name='eliminar_foto'),
    path('resultados/', views.resultados, name='resultados'),
    path('resetear-puntuaciones/', views.resetear_puntuaciones, name='resetear_puntuaciones'),
]
