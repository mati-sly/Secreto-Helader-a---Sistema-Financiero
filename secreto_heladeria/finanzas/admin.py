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
    
    def get_queryset(self, request):
        """Filtrar para que cada usuario solo vea su propio perfil"""
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
    
    def has_change_permission(self, request, obj=None):
        """Solo puede editar su propio perfil"""
        if obj is None:
            return True
        return obj.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        """Nadie puede eliminar perfiles (ni siquiera el propio)"""
        return False

admin.site.register(UserProfile, UserProfileAdmin)


class TransaccionInline(admin.TabularInline):
    model = Transaccion
    extra = 0
    formset = TransaccionInlineFormSet
    
    def get_queryset(self, request):
        """Filtrar transacciones inline por usuario (incluso superusuarios)"""
        qs = super().get_queryset(request)
        return qs.filter(usuario=request.user)

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
    
    def get_queryset(self, request):
        """Cada usuario solo ve sus propias transacciones (admin ve todo)"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el usuario actual al crear"""
        if not change:  # Solo al crear
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        """Solo puede editar sus propias transacciones"""
        if obj is None:
            return True
        return obj.usuario == request.user
    
    def has_delete_permission(self, request, obj=None):
        """Solo puede eliminar sus propias transacciones"""
        if obj is None:
            return True
        return obj.usuario == request.user
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Ocultar el campo usuario del formulario"""
        if db_field.name == "usuario":
            kwargs["initial"] = request.user
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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