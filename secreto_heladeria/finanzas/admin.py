from django.contrib import admin
from .models import Categoria, Transaccion, Producto, CodigoRecuperacion
import csv
from django.http import HttpResponse
from .forms import TransaccionInlineFormSet
from .models import Organization, UserProfile  

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_group', 'organization', 'rut', 'telefono')

    def get_group(self, obj):
        groups = obj.user.groups.all()
        return ", ".join([group.name for group in groups]) if groups else "Sin grupo"
    get_group.short_description = 'Rol'

admin.site.register(UserProfile, UserProfileAdmin)


class TransaccionInline(admin.TabularInline):
    model = Transaccion
    extra = 0
    formset = TransaccionInlineFormSet

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    search_fields = ('nombre',)
    list_filter = ('tipo',)
    inlines = [TransaccionInline]

@admin.action(description="Exportar transacciones seleccionadas a CSV")
def exportar_transacciones_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transacciones.csv"'

    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Categoría', 'Tipo', 'Monto', 'Descripción', 'Fecha'])

    for transaccion in queryset:
        writer.writerow([
            transaccion.usuario.username,
            transaccion.categoria.nombre,
            transaccion.tipo,
            transaccion.monto,
            transaccion.descripcion,
            transaccion.fecha.strftime('%d/%m/%Y %H:%M')
        ])

    return response

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'tipo', 'monto', 'descripcion', 'fecha')
    search_fields = ('descripcion', 'usuario__username')
    list_filter = ('tipo', 'categoria')
    actions = [exportar_transacciones_csv]

# Aquí vienen las dos nuevas acciones para activar/desactivar productos
@admin.action(description="Activar productos seleccionados")
def activar_productos(modeladmin, request, queryset):
    updated = queryset.update(activo=True)
    modeladmin.message_user(request, f"{updated} productos activados correctamente.")

@admin.action(description="Desactivar productos seleccionados")
def desactivar_productos(modeladmin, request, queryset):
    updated = queryset.update(activo=False)
    modeladmin.message_user(request, f"{updated} productos desactivados correctamente.")

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'costo_unitario', 'precio_venta', 'stock', 'activo')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'activo')
    actions = [activar_productos, desactivar_productos]

@admin.register(CodigoRecuperacion)
class CodigoRecuperacionAdmin(admin.ModelAdmin):
    list_display = ('email', 'codigo', 'created_at', 'usado', 'intentos')
    search_fields = ('email', 'codigo')
    list_filter = ('usado',)
