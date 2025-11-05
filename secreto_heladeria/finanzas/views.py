from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
# MODIFICADO: Añadido 'permission_required' al import
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from datetime import datetime, time, timezone as dt_timezone
from django.utils import timezone as dj_timezone
from django.db.models import Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Transaccion, Producto, CodigoRecuperacion, Categoria, Profile
from .forms import ProductoForm, TransaccionForm, UserEditForm, ProfileEditForm, RegistrationForm, RolUsuarioForm 
from django.http import JsonResponse, HttpResponseNotFound # <-- HttpResponseNotFound es útil

# =======================================================
# VISTAS DE AUTENTICACIÓN Y DASHBOARD
# =======================================================

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Credenciales incorrectas')
    return render(request, 'registration/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return redirect('dashboard')
        else:
            messages.error(request, 'No se pudo completar el registro. Por favor, revisa los campos.')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form, 'titulo': 'Crear una Cuenta'})

@login_required
def dashboard(request):
    ingresos_totales = Transaccion.objects.filter(usuario=request.user, tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos_totales = Transaccion.objects.filter(usuario=request.user, tipo='gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    utilidad_total = ingresos_totales - gastos_totales
    transacciones_recientes = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')[:5]
    return render(request, 'dashboard.html', {
        'ingresos_hoy': ingresos_totales,
        'gastos_hoy': gastos_totales,
        'utilidad_hoy': utilidad_total,
        'transacciones': transacciones_recientes,
    })

# =======================================================
# VISTAS DE FINANZAS Y CRUD
# =======================================================

@login_required
def transacciones_list(request):
    tipo_seleccionado = request.GET.get('tipo', '')
    categoria_seleccionada_id = request.GET.get('categoria', '')
    query = request.GET.get('q', '')

    transacciones_qs = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')

    if tipo_seleccionado in ['ingreso', 'gasto']:
        transacciones_qs = transacciones_qs.filter(tipo=tipo_seleccionado)
    if categoria_seleccionada_id:
        transacciones_qs = transacciones_qs.filter(categoria_id=categoria_seleccionada_id)
    if query:
        transacciones_qs = transacciones_qs.filter(descripcion__icontains=query)

    per_page = request.GET.get('per_page', '10') 
    try:
        items_por_pagina = int(per_page)
        if items_por_pagina not in [5, 10, 25]:
            items_por_pagina = 10
    except (ValueError, TypeError):
        items_por_pagina = 10

    paginator = Paginator(transacciones_qs, items_por_pagina)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    querystring = params.urlencode()

    categorias_disponibles = Categoria.objects.all().order_by('nombre')

    contexto = {
        'page_obj': page_obj,
        'querystring': querystring,
        'tipos_transaccion': Transaccion.TIPOS,
        'categorias_disponibles': categorias_disponibles,
        'tipo_seleccionado': tipo_seleccionado,
        'categoria_seleccionada_id': categoria_seleccionada_id,
        'search_query': query,
    }
    return render(request, 'finanzas/transacciones.html', contexto)


@login_required
def productos_list(request):
    categoria_seleccionada = request.GET.get('categoria', '')
    query = request.GET.get('q', '')

    productos_qs = Producto.objects.all().order_by('nombre')

    if categoria_seleccionada:
        productos_qs = productos_qs.filter(categoria=categoria_seleccionada)
    if query:
        productos_qs = productos_qs.filter(nombre__icontains=query)

    per_page = request.GET.get('per_page', '10')
    try:
        items_por_pagina_prod = int(per_page)
        if items_por_pagina_prod not in [5, 10, 25]:
            items_por_pagina_prod = 10
    except (ValueError, TypeError):
        items_por_pagina_prod = 10

    paginator_prod = Paginator(productos_qs, items_por_pagina_prod)
    page_number_prod = request.GET.get('page')

    try:
        page_obj_prod = paginator_prod.get_page(page_number_prod)
    except PageNotAnInteger:
        page_obj_prod = paginator_prod.page(1)
    except EmptyPage:
        page_obj_prod = paginator_prod.page(paginator_prod.num_pages)

    params_prod = request.GET.copy()
    if 'page' in params_prod:
        del params_prod['page']
    querystring_prod = params_prod.urlencode()

    categorias_disponibles = Producto.objects.values_list('categoria', flat=True).distinct().order_by('categoria')

    contexto = {
        'page_obj': page_obj_prod,
        'querystring': querystring_prod,
        'categorias_disponibles': categorias_disponibles,
        'categoria_seleccionada': categoria_seleccionada,
        'producto_model_choices': Producto,
        'search_query': query,
    }
    return render(request, 'finanzas/productos.html', contexto)

@login_required
def reportes(request):
    return render(request, 'finanzas/reportes.html')

def recuperar_password(request):
    User = get_user_model()
    if request.method == 'POST':
        action = request.POST.get('action')
        email = request.POST.get('email')
        if action == 'enviar_codigo':
            try:
                user = User.objects.get(email=email)
                codigo_obj = CodigoRecuperacion.generar_codigo(email)
                html_content = render_to_string('emails/codigo_recuperacion.html', {
                    'codigo': codigo_obj.codigo,
                    'usuario': user.first_name or user.username
                })
                text_content = f'Tu código de recuperación es: {codigo_obj.codigo}\n\nEste código expira en 10 minutos.'
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
                return render(request, 'registration/password_reset_form.html', {
                    'codigo_valido': True,
                    'email': email,
                    'codigo': codigo
                })
            except CodigoRecuperacion.DoesNotExist:
                codigo_obj = CodigoRecuperacion.objects.filter(email=email, codigo=codigo).first()
                if codigo_obj:
                    codigo_obj.incrementar_intento()
                messages.error(request, 'Código inválido')
                return render(request, 'registration/password_reset_form.html', {'codigo_enviado': True, 'email': email})

        elif action == 'cambiar_password':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registration/password_reset_form.html', {'codigo_valido': True, 'email': email})

            try:
                codigo_obj = CodigoRecuperacion.objects.filter(email=email, usado=False).order_by('-created_at').first()
                if not codigo_obj or not codigo_obj.is_valido():
                    messages.error(request, 'Sesión expirada. Solicita un nuevo código.')
                    return render(request, 'registration/password_reset_form.html')

                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                codigo_obj.usado = True
                codigo_obj.save()
                messages.success(request, 'Contraseña cambiada exitosamente')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Error al cambiar contraseña')

    return render(request, 'registration/password_reset_form.html')


# CONTROL DE PERMISOS: Jefe de Ventas y Admin (add_producto)
@login_required
@permission_required('finanzas.add_producto', raise_exception=True)
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto creado exitosamente!')
            return redirect('finanzas:productos')
        else:
            messages.error(request, 'Error al crear el producto. Revisa los campos.')
    else:
        form = ProductoForm()
    contexto = { 'form': form, 'titulo': 'Crear Nuevo Producto' }
    return render(request, 'finanzas/producto_form.html', contexto)

# CONTROL DE PERMISOS: Jefe de Ventas y Admin (change_producto) - Marketing NO tiene este permiso
@login_required
@permission_required('finanzas.change_producto', raise_exception=True)
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado exitosamente!')
            return redirect('finanzas:productos')
        else:
            messages.error(request, 'Error al actualizar el producto. Revisa los campos.')
    else:
        form = ProductoForm(instance=producto)
    contexto = { 'form': form, 'titulo': f'Editar Producto: {producto.nombre}'}
    return render(request, 'finanzas/producto_form.html', contexto)

# CONTROL DE PERMISOS: Solo Admin (delete_producto)
@login_required
@permission_required('finanzas.delete_producto', raise_exception=True)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado.')
    return redirect('finanzas:productos')

# CONTROL DE PERMISOS: Jefe de Ventas y Admin (add_transaccion)
@login_required
@permission_required('finanzas.add_transaccion', raise_exception=True)
def transaccion_create(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            transaccion.save()
            messages.success(request, '¡Transacción creada exitosamente!')
            return redirect('finanzas:transacciones')
        else:
            messages.error(request, 'Error al crear la transacción. Revisa los campos.')
    else:
        form = TransaccionForm()
    form.fields['categoria'].queryset = Categoria.objects.all()
    form.fields['producto'].queryset = Producto.objects.filter(activo=True)
    contexto = { 'form': form, 'titulo': 'Crear Nueva Transacción' }
    return render(request, 'finanzas/transaccion_form.html', contexto)

# CONTROL DE PERMISOS: Jefe de Ventas y Admin (change_transaccion)
@login_required
@permission_required('finanzas.change_transaccion', raise_exception=True)
def transaccion_update(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Transacción actualizada exitosamente!')
            return redirect('finanzas:transacciones')
        else:
            messages.error(request, 'Error al actualizar la transacción. Revisa los campos.')
    else:
        form = TransaccionForm(instance=transaccion)
    form.fields['categoria'].queryset = Categoria.objects.all()
    form.fields['producto'].queryset = Producto.objects.filter(activo=True)
    contexto = { 'form': form, 'titulo': 'Editar Transacción' }
    return render(request, 'finanzas/transaccion_form.html', contexto)

# CONTROL DE PERMISOS: Solo Admin (delete_transaccion)
@login_required
@permission_required('finanzas.delete_transaccion', raise_exception=True)
def transaccion_delete(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, 'Transacción eliminada.')
    return redirect('finanzas:transacciones')


# =======================================================
# VISTAS DE GESTIÓN DE USUARIOS Y PERFILES
# =======================================================

def es_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(es_superuser, login_url='dashboard')
def gestion_usuarios_view(request):
    lista_usuarios = User.objects.exclude(pk=request.user.pk).order_by('username')
    
    for user in lista_usuarios:
        # Si el usuario es Superusuario, su rol será 'Admin' para la visualización en la tabla
        if user.is_superuser:
            user.rol_actual = 'Admin'
        else:
            user.rol_actual = user.groups.first().name if user.groups.exists() else 'Sin Rol'
    
    context = {
        'usuarios': lista_usuarios
    }
    return render(request, 'finanzas/gestion_usuarios.html', context)


@login_required
@user_passes_test(es_superuser, login_url='dashboard')
def editar_rol_view(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    
    # Restricción: No se permite editar al único Superuser logueado
    if usuario == request.user:
        messages.error(request, "No puedes editar tu propio rol/estado de administrador desde aquí.")
        return redirect('finanzas:gestion_usuarios')

    # Restricción: Si el usuario es Superuser, no permitir editar el rol (debe hacerse en /admin)
    if usuario.is_superuser:
        messages.error(request, "El rol de Superusuario solo puede ser modificado en el panel de administración de Django.")
        return redirect('finanzas:gestion_usuarios')


    if request.method == 'POST':
        form = RolUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f"El rol del usuario '{usuario.username}' ha sido actualizado a '{form.cleaned_data['rol_seleccionado']}'.")
            return redirect('finanzas:gestion_usuarios')
        else:
            messages.error(request, "Error al actualizar el rol. Revisa el formulario.")
    else:
        form = RolUsuarioForm(instance=usuario)
    
    context = {
        'form': form,
        'usuario': usuario,
        'titulo': f'Editar Rol de {usuario.username}'
    }
    return render(request, 'finanzas/editar_rol.html', context)


@login_required
def editar_perfil(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Perfil actualizado'})
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('editar_perfil')
        else:
             if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = user_form.errors.as_json() + profile_form.errors.as_json()
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)
             messages.error(request, 'Hubo un error al actualizar tu perfil. Revisa los campos.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)
    context = { 'user_form': user_form, 'profile_form': profile_form, 'titulo': 'Editar Perfil', 'perfil': profile }
    return render(request, 'finanzas/editar_perfil.html', context)

# =======================================================
# 🌟 MANEJADOR DE ERRORES 404 (NUEVO)
# Usado por handler404 en urls.py
# =======================================================

def custom_404_view(request, exception=None):
    if not request.user.is_authenticated:
        # Si el usuario NO está logueado, redirige o muestra un error de Acceso Denegado/No Encontrado
        return render(request, '404_unauthenticated.html', {
            'message': 'No se pudo encontrar la página solicitada o necesitas iniciar sesión.',
            'is_authenticated': False
        }, status=404)
        
    else:
        # Si el usuario está logueado (pero la URL no existe), muestra un 404 genérico
        return render(request, '404_authenticated.html', {
            'message': 'La página solicitada no existe. Verifica la dirección URL.',
            'is_authenticated': True
        }, status=404)