from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Avg, Count, F
from django.db.models.functions import Coalesce
from .models import Candidata, Foto, Puntuacion
from .forms import FotoForm, CandidataForm, PuntuacionForm

def lista_candidatas(request):
    candidatas = Candidata.objects.annotate(
        tiene_puntuacion=Count('puntuaciones')
    ).order_by('nombre', 'apellido')
    return render(request, 'candidatas/lista_candidatas.html', {'candidatas': candidatas})

def detalle_candidata(request, pk):
    candidatura = get_object_or_404(Candidata, pk=pk)
    fotos = candidatura.fotos.all()
    puntuacion = Puntuacion.objects.filter(candidatura=candidatura).first()
    return render(request, 'candidatas/detalle_candidata.html', {
        'candidata': candidatura,
        'candidatura': candidatura,
        'fotos': fotos,
        'puntuacion': puntuacion,
        'tiene_puntuacion': puntuacion is not None
    })

def subir_foto(request, pk):
    candidatura = get_object_or_404(Candidata, pk=pk)
    if request.method == 'POST':
        files = request.FILES.getlist('fotos')
        descripcion = request.POST.get('descripcion', '')

        if files:
            for f in files:
                Foto.objects.create(candidatura=candidatura, imagen=f, descripcion=descripcion)
            return redirect('detalle_candidata', pk=candidatura.pk)
        else:
            return render(request, 'candidatas/subir_foto.html', {
                'candidata': candidatura,
                'candidatura': candidatura,
                'error': 'No se seleccionaron archivos.'
            })

    return render(request, 'candidatas/subir_foto.html', {
        'candidata': candidatura, 
        'candidatura': candidatura
    })

def agregar_candidata(request):
    if request.method == 'POST':
        form = CandidataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_candidatas')
    else:
        form = CandidataForm()
    return render(request, 'candidatas/agregar_candidata.html', {'form': form})

def editar_candidata(request, pk):
    candidatura = get_object_or_404(Candidata, pk=pk)
    if request.method == 'POST':
        form = CandidataForm(request.POST, request.FILES, instance=candidatura)
        if form.is_valid():
            form.save()
            return redirect('detalle_candidata', pk=candidatura.pk)
    else:
        form = CandidataForm(instance=candidatura)
    return render(request, 'candidatas/editar_candidata.html', {
        'form': form, 
        'candidata': candidatura,
        'candidatura': candidatura,
        'errors': form.errors if request.method == 'POST' and not form.is_valid() else None
    })

def eliminar_candidata(request, pk):
    candidatura = get_object_or_404(Candidata, pk=pk)
    if request.method == 'POST':
        candidatura.delete()
        return redirect('lista_candidatas')
    return render(request, 'candidatas/eliminar_candidata.html', {'candidata': candidatura, 'candidatura': candidatura})

def eliminar_foto(request, pk):
    foto = get_object_or_404(Foto, pk=pk)
    candidata_pk = foto.candidatura.pk
    foto.delete()
    return redirect('detalle_candidata', pk=candidata_pk)

def puntuar_candidata(request, pk):
    candidatura = get_object_or_404(Candidata, pk=pk)
    puntuacion_existente = Puntuacion.objects.filter(candidatura=candidatura).first()
    
    if request.method == 'POST':
        form = PuntuacionForm(request.POST)
        if form.is_valid():
            if puntuacion_existente:
                puntuacion_existente.belleza = form.cleaned_data['belleza']
                puntuacion_existente.simpatia = form.cleaned_data['simpatia']
                puntuacion_existente.elegancia = form.cleaned_data['elegancia']
                puntuacion_existente.vestimenta = form.cleaned_data['vestimenta']
                puntuacion_existente.maquillaje = form.cleaned_data['maquillaje']
                puntuacion_existente.hinchada = form.cleaned_data['hinchada']
                puntuacion_existente.save()
            else:
                puntuacion = form.save(commit=False)
                puntuacion.candidatura = candidatura
                puntuacion.save()
            return redirect('detalle_candidata', pk=candidatura.pk)
        errors = form.errors
    else:
        if puntuacion_existente:
            form = PuntuacionForm(instance=puntuacion_existente)
        else:
            form = PuntuacionForm()
        errors = None
    
    return render(request, 'candidatas/puntuar_candidata.html', {
        'form': form, 
        'candidata': candidatura, 
        'candidatura': candidatura,
        'errors': errors,
        'puntuacion_existente': puntuacion_existente is not None
    })

def resultados(request):
    candidatas = Candidata.objects.annotate(
        total_belleza=Coalesce(Sum('puntuaciones__belleza'), 0),
        total_simpatia=Coalesce(Sum('puntuaciones__simpatia'), 0),
        total_elegancia=Coalesce(Sum('puntuaciones__elegancia'), 0),
        total_vestimenta=Coalesce(Sum('puntuaciones__vestimenta'), 0),
        total_maquillaje=Coalesce(Sum('puntuaciones__maquillaje'), 0),
        total_hinchada=Coalesce(Sum('puntuaciones__hinchada'), 0),
        cantidad_votos=Count('puntuaciones'),
    ).annotate(
        promedio_total=F('total_belleza') + F('total_simpatia') + F('total_elegancia') + F('total_vestimenta') + F('total_maquillaje') + F('total_hinchada')
    ).order_by('-promedio_total')

    return render(request, 'candidatas/resultados.html', {
        'candidatas': candidatas,
    })

def resetear_puntuaciones(request):
    if request.method == 'POST':
        Puntuacion.objects.all().delete()
        return redirect('resultados')
    return render(request, 'candidatas/resetear_puntuaciones.html')