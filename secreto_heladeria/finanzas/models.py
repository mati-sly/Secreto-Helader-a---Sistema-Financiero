import random
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver # <-- IMPORTACIÓN AÑADIDA


class Categoria(models.Model):
    # --- CÓDIGO RESTAURADO ---
    TIPOS = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto')
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPOS, default='gasto')
    # --- FIN DE LA RESTAURACIÓN ---

    def __str__(self):
        return self.nombre


class Transaccion(models.Model):
    # --- CÓDIGO RESTAURADO ---
    TIPOS = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto')
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS,
        verbose_name="Tipo de Transacción"
    )

    producto = models.ForeignKey(
        'Producto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Producto Asociado (opcional, si es venta)"
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoría (opcional, para agrupar)"
    )

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="El monto debe ser mayor a cero")]
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción (opcional)"
        )
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

    def clean(self):
        if self.monto is not None and self.monto <= 0:
            raise ValidationError({'monto': 'El monto debe ser un número positivo mayor a cero.'})

        if self.producto and self.tipo == 'gasto':
             raise ValidationError({
                 'tipo': 'Si asocias un Producto, la transacción debe ser un Ingreso.',
                 'producto': 'No puedes asociar un Producto a un Gasto.'
                 })

        if self.tipo == 'gasto' and self.producto:
            raise ValidationError({'producto': 'Las transacciones de Gasto no pueden tener un Producto asociado.'})

        if not self.producto and not self.categoria and not self.descripcion:
            raise ValidationError('Debes seleccionar un Producto (si es venta), una Categoría o ingresar una Descripción.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    # --- FIN DE LA RESTAURACIÓN ---

    def __str__(self):
        detail = ""
        if self.producto:
            detail = f"Prod: {self.producto.nombre}"
        elif self.categoria:
            detail = f"Cat: {self.categoria.nombre}"
        elif self.descripcion:
             detail = self.descripcion[:20] + ('...' if len(self.descripcion) > 20 else '')
        else:
            detail = "Sin detalle"
        return f"{self.fecha.strftime('%d/%m/%y')} - {self.get_tipo_display()}: ${self.monto} ({detail})"


class Producto(models.Model):
    # --- CÓDIGO RESTAURADO ---
    CATEGORIAS = [
        ('helado', 'Helado'), ('cafe', 'Café'),
        ('pasteleria', 'Pastelería'), ('otro', 'Otro')
    ]
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    costo_unitario = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0, message="El costo debe ser mayor o igual a cero")]
    )
    precio_venta = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="El precio debe ser mayor a cero")]
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="El stock no puede ser negativo")]
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def clean(self):
        if self.costo_unitario is not None and self.costo_unitario < 0:
            raise ValidationError({'costo_unitario': 'El costo unitario no puede ser negativo.'})
        if self.precio_venta is not None and self.precio_venta <= 0:
            raise ValidationError({'precio_venta': 'El precio de venta debe ser mayor a cero.'})
        if self.precio_venta is not None and self.costo_unitario is not None and self.precio_venta < self.costo_unitario:
             raise ValidationError({'precio_venta': 'El precio de venta no puede ser menor que el costo unitario.'})
        if self.stock is not None and self.stock < 0:
            raise ValidationError({'stock': 'El stock no puede ser negativo.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    # --- FIN DE LA RESTAURACIÓN ---

    def __str__(self):
        return f"{self.nombre} (${self.precio_venta})"


class CodigoRecuperacion(models.Model):
    # --- CÓDIGO RESTAURADO ---
    email = models.EmailField()
    codigo = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)
    intentos = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Código de Recuperación"
        verbose_name_plural = "Códigos de Recuperación"

    def is_valido(self):
        tiempo_limite = self.created_at + timedelta(minutes=1)
        return timezone.now() < tiempo_limite and not self.usado

    def incrementar_intento(self):
        self.intentos += 1
        self.save()

    @classmethod
    def generar_codigo(cls, email):
        cls.objects.filter(email=email, usado=False).update(usado=True)
        codigo = f"{random.randint(1000, 9999)}"
        return cls.objects.create(email=email, codigo=codigo)
    # --- FIN DE LA RESTAURACIÓN ---

    def __str__(self):
        return f"Código {self.codigo} para {self.email}"


class Organization(models.Model):
    # --- CÓDIGO RESTAURADO ---
    name = models.CharField(max_length=150, unique=True)
    # --- FIN DE LA RESTAURACIÓN ---

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # --- CÓDIGO RESTAURADO ---
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    # --- FIN DE LA RESTAURACIÓN ---

    def __str__(self):
        return f"{self.user.username} @ {self.organization.name}"


# --- INICIO: CÓDIGO AÑADIDO PARA FOTOS DE PERFIL ---

class Profile(models.Model):
    """
    Modelo para extender el User de Django con una foto de perfil.
    Se vincula 1 a 1 con el modelo User que ya importaste.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Usamos upload_to='perfiles/' para guardar las fotos en la carpeta 'media/perfiles/'
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True, default='perfiles/default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'

# --- Señales (Signals) ---
# Estas funciones se aseguran de que cada vez que se crea un nuevo
# usuario, automáticamente se cree un 'Profile' vacío para él.

@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Esto es por si un usuario antiguo (como tu superadmin) no tiene perfil
        Profile.objects.create(user=instance)

# --- FIN: CÓDIGO AÑADIDO ---

