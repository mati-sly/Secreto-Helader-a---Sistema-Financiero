from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('transacciones/', views.transacciones_list, name='transacciones'),
    path('productos/', views.productos_list, name='productos'),
    path('reportes/', views.reportes, name='reportes'),
]
