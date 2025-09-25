from django.contrib import admin
from .models import Categoria, Transaccion, Producto, CodigoRecuperacion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'created_at')
    search_fields = ('nombre',)
    list_filter = ('tipo',)

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'tipo', 'monto', 'descripcion', 'fecha')
    search_fields = ('descripcion', 'usuario__username')
    list_filter = ('tipo', 'categoria')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'costo_unitario', 'precio_venta', 'stock', 'activo')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'activo')

@admin.register(CodigoRecuperacion)
class CodigoRecuperacionAdmin(admin.ModelAdmin):
    list_display = ('email', 'codigo', 'created_at', 'usado', 'intentos')
    search_fields = ('email', 'codigo')
    list_filter = ('usado',)
