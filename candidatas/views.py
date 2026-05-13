from django.shortcuts import render, get_object_or_404, redirect
from .models import Candidata, Foto
from .forms import FotoForm, CandidataForm

def lista_candidatas(request):
    candidatas = Candidata.objects.all()
    return render(request, 'candidatas/lista_candidatas.html', {'candidatas': candidatas})

def detalle_candidata(request, pk):
    candidata = get_object_or_404(Candidata, pk=pk)
    fotos = candidata.fotos.all()
    return render(request, 'candidatas/detalle_candidata.html', {'candidata': candidata, 'fotos': fotos})

def subir_foto(request, pk):
    candidata = get_object_or_404(Candidata, pk=pk)
    if request.method == 'POST':
        # Procesamos manualmente para evitar errores de validación de Django
        files = request.FILES.getlist('fotos')
        descripcion = request.POST.get('descripcion', '')
        
        if files:
            for f in files:
                Foto.objects.create(candidata=candidata, imagen=f, descripcion=descripcion)
            return redirect('detalle_candidata', pk=candidata.pk)
        else:
            # Si por alguna razón no hay archivos, recargamos con un mensaje simple
            return render(request, 'candidatas/subir_foto.html', {
                'candidata': candidata,
                'error': 'No se seleccionaron archivos.'
            })
            
    return render(request, 'candidatas/subir_foto.html', {'candidata': candidata})

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
    candidata = get_object_or_404(Candidata, pk=pk)
    if request.method == 'POST':
        form = CandidataForm(request.POST, request.FILES, instance=candidata)
        if form.is_valid():
            form.save()
            return redirect('detalle_candidata', pk=candidata.pk)
    else:
        form = CandidataForm(instance=candidata)
    return render(request, 'candidatas/editar_candidata.html', {'form': form, 'candidata': candidata})

def eliminar_candidata(request, pk):
    candidata = get_object_or_404(Candidata, pk=pk)
    if request.method == 'POST':
        candidata.delete()
        return redirect('lista_candidatas')
    return render(request, 'candidatas/eliminar_candidata.html', {'candidata': candidata})

def eliminar_foto(request, pk):
    foto = get_object_or_404(Foto, pk=pk)
    candidata_pk = foto.candidata.pk
    foto.delete()
    return redirect('detalle_candidata', pk=candidata_pk)
