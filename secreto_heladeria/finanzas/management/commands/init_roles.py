from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from finanzas.models import Producto, Transaccion 

class Command(BaseCommand):
    help = 'Crea o actualiza los grupos de roles y asigna permisos estrictamente definidos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando script de asignación de Roles y Permisos...'))
        
        # 1. DEFINICIÓN DE PERMISOS POR ROL
        
        # PERMISOS PARA JEFES DE VENTAS: CRUD en Producto (sin delete), CRUD en Transacción (sin delete)
        PERMISOS_VENTAS = [
            'view_producto', 'add_producto', 'change_producto',
            'view_transaccion', 'add_transaccion', 'change_transaccion',
        ]
        
        # PERMISOS PARA MARKETING: SOLO LECTURA (view_)
        PERMISOS_MARKETING = [
            'view_producto',      # Puede ver el listado y detalle de productos
            'view_transaccion',   # Puede ver el listado y detalle de transacciones
            # NOTA: Todos los permisos de add/change/delete están AUSENTES para Marketing
        ]

        # 2. AGRUPAR ROLES
        grupos = {
            'Jefe de Ventas': PERMISOS_VENTAS,
            'Marketing': PERMISOS_MARKETING,
        }
        
        # 3. OBTENER CONTENT TYPES (Asegura que los modelos existen)
        try:
            content_type_producto = ContentType.objects.get_for_model(Producto)
            content_type_transaccion = ContentType.objects.get_for_model(Transaccion)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al obtener ContentType. ¿Ejecutaste las migraciones? Error: {e}'))
            return

        # 4. ASIGNAR PERMISOS A CADA GRUPO
        for nombre_grupo, codigos_permiso in grupos.items():
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            
            # Limpiar todos los permisos existentes antes de reasignar
            grupo.permissions.clear()
            
            for codename in codigos_permiso:
                try:
                    # Determinar el ContentType
                    if 'producto' in codename:
                        ct = content_type_producto
                    elif 'transaccion' in codename:
                        ct = content_type_transaccion
                    else:
                         continue

                    permiso = Permission.objects.get(codename=codename, content_type=ct)
                    grupo.permissions.add(permiso)
                    self.stdout.write(f'  [OK] {nombre_grupo}: Asignado permiso {codename}')
                except Permission.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f'  [ADVERTENCIA] Permiso {codename} no encontrado. Posiblemente falta en el modelo.'))

            if created:
                self.stdout.write(self.style.SUCCESS(f'\nGrupo "{nombre_grupo}" creado y permisos asignados.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'\nGrupo "{nombre_grupo}" actualizado.'))

        self.stdout.write(self.style.SUCCESS('\n>>> Inicialización de Roles completada. Los permisos están configurados para Solo Lectura de Marketing. <<<'))