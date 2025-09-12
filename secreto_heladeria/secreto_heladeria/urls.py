from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from finanzas.views import dashboard, custom_login, recuperar_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('finanzas/', include('finanzas.urls')),
    path('login/', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Recuperación de contraseña personalizada con código de 4 dígitos
    path('password_reset/', recuperar_password, name='password_reset'),
]