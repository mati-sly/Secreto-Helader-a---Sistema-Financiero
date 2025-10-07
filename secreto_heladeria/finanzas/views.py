# Importaciones de Django para vistas, autenticación y mensajes
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Importaciones para manejo de fechas
from datetime import datetime, time, timezone as dt_timezone
from django.utils import timezone as dj_timezone

# Importaciones para consultas y agregaciones
from django.db.models import Sum

# Importaciones para envío de email
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Modelos de la aplicación
from .models import Transaccion, Producto, CodigoRecuperacion


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Credenciales incorrectas')
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    # Total de ingresos y gastos de todas las transacciones
    ingresos_totales = Transaccion.objects.filter(tipo='Venta').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos_totales = Transaccion.objects.filter(tipo='Gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    utilidad_total = ingresos_totales - gastos_totales

    # Todas las transacciones
    transacciones = Transaccion.objects.all()

    return render(request, 'dashboard.html', {
        'ingresos_hoy': ingresos_totales,
        'gastos_hoy': gastos_totales,
        'utilidad_hoy': utilidad_total,
        'transacciones': transacciones,
    })


@login_required
def transacciones_list(request):
    transacciones = Transaccion.objects.all()
    return render(request, 'finanzas/transacciones.html', {'transacciones': transacciones})

@login_required
def productos_list(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'finanzas/productos.html', {'productos': productos})

@login_required
def reportes(request):
    return render(request, 'finanzas/reportes.html')

def recuperar_password(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        email = request.POST.get('email')

        # --------------------
        # Paso 1: Enviar código
        # --------------------
        if action == 'enviar_codigo':
            try:
                user = User.objects.get(email=email)
                codigo_obj = CodigoRecuperacion.generar_codigo(email)

                # Preparar contenido HTML y texto plano
                html_content = render_to_string('emails/codigo_recuperacion.html', {
                    'codigo': codigo_obj.codigo,
                    'usuario': user.first_name or user.username
                })
                text_content = f'Tu código de recuperación es: {codigo_obj.codigo}\n\nEste código expira en 10 minutos.'
                
                # Enviar email
                msg = EmailMultiAlternatives(
                    subject='Código de recuperación - Secreto Heladería',
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, 'Código enviado a tu email')
                return render(request, 'registration/password_reset_form.html', {
                    'codigo_enviado': True,
                    'email': email
                })
            except User.DoesNotExist:
                messages.error(request, 'Email no encontrado')

        # --------------------
        # Paso 2: Verificar código
        # --------------------
        elif action == 'verificar_codigo':
            codigo = request.POST.get('codigo')
            try:
                codigo_obj = CodigoRecuperacion.objects.get(email=email, codigo=codigo, usado=False)

                if not codigo_obj.is_valido():
                    messages.error(request, 'Código expirado')
                    return render(request, 'registration/password_reset_form.html', {'codigo_enviado': True, 'email': email})

                if codigo_obj.intentos >= 3:
                    messages.error(request, 'Demasiados intentos fallidos')
                    return render(request, 'registration/password_reset_form.html')

                # Código válido, mostrar formulario para nueva contraseña
                return render(request, 'registration/password_reset_form.html', {
                    'codigo_valido': True,
                    'email': email,
                    'codigo': codigo
                })

            except CodigoRecuperacion.DoesNotExist:
                # Incrementar intentos si existe el código
                codigo_obj = CodigoRecuperacion.objects.filter(email=email, codigo=codigo).first()
                if codigo_obj:
                    codigo_obj.incrementar_intento()
                messages.error(request, 'Código inválido')
                return render(request, 'registration/password_reset_form.html', {'codigo_enviado': True, 'email': email})

        # --------------------
        # Paso 3: Cambiar contraseña
        # --------------------
        elif action == 'cambiar_password':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registration/password_reset_form.html', {'codigo_valido': True, 'email': email})

            try:
                # Tomar el código más reciente y válido
                codigo_obj = CodigoRecuperacion.objects.filter(email=email, usado=False).order_by('-created_at').first()
                if not codigo_obj or not codigo_obj.is_valido():
                    messages.error(request, 'Sesión expirada. Solicita un nuevo código.')
                    return render(request, 'registration/password_reset_form.html')

                # Cambiar contraseña
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()

                # Marcar código como usado
                codigo_obj.usado = True
                codigo_obj.save()

                messages.success(request, 'Contraseña cambiada exitosamente')
                return redirect('login')

            except User.DoesNotExist:
                messages.error(request, 'Error al cambiar contraseña')

    return render(request, 'registration/password_reset_form.html')