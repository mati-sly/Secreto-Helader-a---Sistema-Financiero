from django.core.management.base import BaseCommand
from finanzas.models import Transaccion, Producto  # importa tus modelos

import json

class Command(BaseCommand):
    help = 'Exporta los datos de la base de datos a JSON'

    def handle(self, *args, **kwargs):
        data = []

        # ejemplo: exportar Transacciones
        for t in Transaccion.objects.all():
            data.append({
                'tipo': t.tipo,
                'monto': float(t.monto),
                'fecha': t.fecha.isoformat(),
                'descripcion': t.descripcion,
            })

        with open('00_transacciones.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS('Datos exportados correctamente.'))
