from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    # --- URLS EXISTENTES ---
    path('transacciones/', views.transacciones_list, name='transacciones'),
    path('productos/', views.productos_list, name='productos'),
    path('reportes/', views.reportes, name='reportes'),

    # --- CRUD DE PRODUCTOS (Ya lo tienes) ---
    path('productos/nuevo/', views.producto_create, name='producto_crear'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_eliminar'),

    # --- CRUD DE TRANSACCIONES (ESTO ES LO NUEVO) ---
    path('transacciones/nueva/', views.transaccion_create, name='transaccion_crear'), # <- Ruta para el botón Crear
    path('transacciones/<int:pk>/editar/', views.transaccion_update, name='transaccion_editar'), # <- Ruta para el botón Editar
    path('transacciones/<int:pk>/eliminar/', views.transaccion_delete, name='transaccion_eliminar'), # <- Ruta para el botón Eliminar
]

