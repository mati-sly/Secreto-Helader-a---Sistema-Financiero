# secreto_heladeria/finanzas/urls.py

from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    # --- URLS EXISTENTES ---
    path('transacciones/', views.transacciones_list, name='transacciones'),
    path('productos/', views.productos_list, name='productos'),
    path('reportes/', views.reportes, name='reportes'),

    # --- CRUD DE PRODUCTOS ---
    path('productos/nuevo/', views.producto_create, name='producto_crear'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_eliminar'),

    # --- CRUD DE TRANSACCIONES ---
    path('transacciones/nueva/', views.transaccion_create, name='transaccion_crear'),
    path('transacciones/<int:pk>/editar/', views.transaccion_update, name='transaccion_editar'),
    path('transacciones/<int:pk>/eliminar/', views.transaccion_delete, name='transaccion_eliminar'),
    
    # 🌟 RUTAS DE GESTIÓN DE USUARIOS (¡AGREGAR ESTO!)
    path('gestion-usuarios/', views.gestion_usuarios_view, name='gestion_usuarios'),
    path('gestion-usuarios/editar/<int:user_id>/', views.editar_rol_view, name='editar_rol'),
]
handler404 = 'finanzas.views.custom_404_view'