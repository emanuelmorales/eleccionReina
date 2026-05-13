from django.db import models

class Candidata(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    edad = models.IntegerField()
    imagen = models.ImageField(upload_to='candidatas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Foto(models.Model):
    candidata = models.ForeignKey(Candidata, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='fotos_candidatas/')
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Foto de {self.candidata.nombre} - {self.id}"
