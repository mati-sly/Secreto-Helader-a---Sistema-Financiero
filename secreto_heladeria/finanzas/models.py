import random
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    TIPOS = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto')
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPOS)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Transaccion(models.Model):
    TIPOS = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto')
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="El monto debe ser mayor a cero")]
    )
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha']

    def clean(self):
        """Validación adicional para asegurar montos positivos"""
        if self.monto is not None and self.monto <= 0:
            raise ValidationError({'monto': 'El monto debe ser un número positivo mayor a cero.'})

    def save(self, *args, **kwargs):
        """Ejecutar validación antes de guardar"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()}: ${self.monto}"


class Producto(models.Model):
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
    
    def clean(self):
        """Validación adicional"""
        if self.costo_unitario is not None and self.costo_unitario < 0:
            raise ValidationError({'costo_unitario': 'El costo unitario no puede ser negativo.'})
        if self.precio_venta is not None and self.precio_venta <= 0:
            raise ValidationError({'precio_venta': 'El precio de venta debe ser mayor a cero.'})
        if self.stock is not None and self.stock < 0:
            raise ValidationError({'stock': 'El stock no puede ser negativo.'})
    
    def save(self, *args, **kwargs):
        """Ejecutar validación antes de guardar"""
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio_venta}"

class CodigoRecuperacion(models.Model):
    email = models.EmailField()
    codigo = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)
    intentos = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Código de Recuperación"
        verbose_name_plural = "Códigos de Recuperación"
    
    def is_valido(self):
        # Válido por 1 minuto
        tiempo_limite = self.created_at + timedelta(minutes=1)
        return timezone.now() < tiempo_limite and not self.usado
    
    def incrementar_intento(self):
        self.intentos += 1
        self.save()
    
    @classmethod
    def generar_codigo(cls, email):
        # Invalidar códigos anteriores del mismo email
        cls.objects.filter(email=email, usado=False).update(usado=True)
        
        # Crear nuevo código de 4 dígitos
        codigo = f"{random.randint(1000, 9999)}"
        return cls.objects.create(email=email, codigo=codigo)
    
    def __str__(self):
        return f"Código {self.codigo} para {self.email}"
    
class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} @ {self.organization.name}"