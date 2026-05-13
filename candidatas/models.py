from django.db import models

class Candidata(models.Model):
    TURNO_CHOICES = [
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    edad = models.IntegerField()
    fecha_nacimiento = models.DateField(null=True, blank=True)
    curso = models.CharField(max_length=50, blank=True, default='')
    division = models.CharField(max_length=50, blank=True, default='')
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES, blank=True, default='')
    especialidad = models.CharField(max_length=100, blank=True, default='')
    estatura = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    pasatiempos = models.TextField(blank=True, default='')
    proyectos_aspiraciones = models.TextField(blank=True, default='')
    imagen = models.ImageField(upload_to='candidatas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def total_puntos(self):
        return self.puntuaciones.aggregate(
            total=models.Sum('belleza') + models.Sum('simpatia') + models.Sum('elegancia') + 
                       models.Sum('vestimenta') + models.Sum('maquillaje') + models.Sum('hinchada')
        )['total'] or 0

class Foto(models.Model):
    candidata = models.ForeignKey(Candidata, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='fotos_candidatas/')
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Foto de {self.candidata.nombre} - {self.id}"

class Puntuacion(models.Model):
    candidata = models.ForeignKey(Candidata, on_delete=models.CASCADE, related_name='puntuaciones')
    belleza = models.IntegerField(default=0)
    simpatia = models.IntegerField(default=0)
    elegancia = models.IntegerField(default=0)
    vestimenta = models.IntegerField(default=0)
    maquillaje = models.IntegerField(default=0)
    hinchada = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Puntuaciones'

    @property
    def total(self):
        return self.belleza + self.simpatia + self.elegancia + self.vestimenta + self.maquillaje + self.hinchada

    def __str__(self):
        return f"Puntuación de {self.candidata.nombre} - Total: {self.total}"
