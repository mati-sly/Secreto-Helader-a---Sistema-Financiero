
from django.contrib import admin
from .models import Organization, UserProfile, Transaccion, Categoria, Producto, CodigoRecuperacion


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "telefono", "creado_en", "actualizado_en")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role")


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo", "monto", "fecha", "organization")
    list_filter = ("organization", "tipo")  # 👈 para filtrar por organización y tipo


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "created_at")
    list_filter = ("tipo",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "costo_unitario", "precio_venta", "stock", "activo")
    list_filter = ("categoria", "activo")


@admin.register(CodigoRecuperacion)
class CodigoRecuperacionAdmin(admin.ModelAdmin):
    list_display = ("email", "codigo", "created_at", "usado", "intentos")
    list_filter = ("usado",)

#Alma: agregué el archivo admin.py para registrar el modelo Organization en el panel de administración de Django.
#que le faltaba