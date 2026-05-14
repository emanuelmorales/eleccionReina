from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from candidatas.models import Candidata, Foto, Puntuacion


class Command(BaseCommand):
    help = 'Crea los grupos de Administrador y Jurado con sus permisos'

    def handle(self, *args, **options):
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        jury_group, created = Group.objects.get_or_create(name='Jurado')

        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupo "{admin_group.name}" creado'))
            self.stdout.write(self.style.SUCCESS(f'Grupo "{jury_group.name}" creado'))
        else:
            self.stdout.write('Los grupos ya existen')

        ct_candidata = ContentType.objects.get_for_model(Candidata)
        ct_foto = ContentType.objects.get_for_model(Foto)
        ct_puntuacion = ContentType.objects.get_for_model(Puntuacion)

        admin_perms = [
            Permission.objects.get_or_create(codename=f'add_{Candidata._meta.model_name}', name=f'Can add {Candidata._meta.verbose_name}', content_type=ct_candidata)[0],
            Permission.objects.get_or_create(codename=f'change_{Candidata._meta.model_name}', name=f'Can change {Candidata._meta.verbose_name}', content_type=ct_candidata)[0],
            Permission.objects.get_or_create(codename=f'delete_{Candidata._meta.model_name}', name=f'Can delete {Candidata._meta.verbose_name}', content_type=ct_candidata)[0],
            Permission.objects.get_or_create(codename=f'view_{Candidata._meta.model_name}', name=f'Can view {Candidata._meta.verbose_name}', content_type=ct_candidata)[0],
            Permission.objects.get_or_create(codename=f'add_{Foto._meta.model_name}', name=f'Can add {Foto._meta.verbose_name}', content_type=ct_foto)[0],
            Permission.objects.get_or_create(codename=f'change_{Foto._meta.model_name}', name=f'Can change {Foto._meta.verbose_name}', content_type=ct_foto)[0],
            Permission.objects.get_or_create(codename=f'delete_{Foto._meta.model_name}', name=f'Can delete {Foto._meta.verbose_name}', content_type=ct_foto)[0],
            Permission.objects.get_or_create(codename=f'view_{Foto._meta.model_name}', name=f'Can view {Foto._meta.verbose_name}', content_type=ct_foto)[0],
            Permission.objects.get_or_create(codename=f'add_{Puntuacion._meta.model_name}', name=f'Can add {Puntuacion._meta.verbose_name}', content_type=ct_puntuacion)[0],
            Permission.objects.get_or_create(codename=f'change_{Puntuacion._meta.model_name}', name=f'Can change {Puntuacion._meta.verbose_name}', content_type=ct_puntuacion)[0],
            Permission.objects.get_or_create(codename=f'delete_{Puntuacion._meta.model_name}', name=f'Can delete {Puntuacion._meta.verbose_name}', content_type=ct_puntuacion)[0],
            Permission.objects.get_or_create(codename=f'view_{Puntuacion._meta.model_name}', name=f'Can view {Puntuacion._meta.verbose_name}', content_type=ct_puntuacion)[0],
        ]
        admin_group.permissions.set(admin_perms)

        jury_perms = [
            Permission.objects.get_or_create(codename=f'view_{Candidata._meta.model_name}', name=f'Can view {Candidata._meta.verbose_name}', content_type=ct_candidata)[0],
            Permission.objects.get_or_create(codename=f'view_{Puntuacion._meta.model_name}', name=f'Can view {Puntuacion._meta.verbose_name}', content_type=ct_puntuacion)[0],
            Permission.objects.get_or_create(codename=f'add_{Puntuacion._meta.model_name}', name=f'Can add {Puntuacion._meta.verbose_name}', content_type=ct_puntuacion)[0],
            Permission.objects.get_or_create(codename=f'change_{Puntuacion._meta.model_name}', name=f'Can change {Puntuacion._meta.verbose_name}', content_type=ct_puntuacion)[0],
        ]
        jury_group.permissions.set(jury_perms)

        self.stdout.write(self.style.SUCCESS('Permisos asignados correctamente'))
        self.stdout.write(self.style.SUCCESS('Listo! Ahora puedes agregar usuarios a los grupos desde /admin'))