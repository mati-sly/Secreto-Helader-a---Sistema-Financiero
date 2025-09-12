# Secreto Heladería - Sistema Financiero

Sistema de gestión financiera desarrollado específicamente para **Secreto Heladería**, una heladería artesanal ubicada en La Serena, Chile.

Diseñado para solucionar la **crisis de gestión manual** identificada en el análisis empresarial, digitalizando el control de transacciones, productos e inventario.

## Contexto del Proyecto

Este sistema fue desarrollado basándose en un análisis exhaustivo de Secreto Heladería que identificó problemas críticos:

- **Gestión 100% manual** con cuadernos físicos
- **Ausencia de control financiero** digital
- **Sin seguimiento de inventario** automatizado
- **Estacionalidad extrema** que requiere análisis de datos
- **Falta de sistemas profesionales** básicos

## Características Principales

### Autenticación Completa

- Login seguro con diseño corporativo
- **Recuperación de contraseña funcional**
- Sistema de permisos integrado
- Redirecciones automáticas

### Control Financiero

- **Dashboard en tiempo real** con estadísticas del día
- Registro de ingresos y gastos por categorías
- Transacciones con fecha, monto y descripción
- **Cálculo automático de utilidades**

### Gestión de Productos

- Catálogo completo de productos
- Control de **stock con alertas de inventario bajo**
- Categorización (Helados, Café, Pastelería, Otros)
- Cálculo de márgenes de ganancia

### Reportes y Análisis

- Estadísticas diarias automáticas
- Historial de transacciones filtrable
- **Preparado para expansión** con gráficos y análisis avanzados

## Tecnologías Utilizadas

- **Backend:** Django 4.2+ (Python)
- **Base de datos:** SQLite3 (desarrollo) / PostgreSQL (producción)
- **Frontend:** HTML5, CSS3, JavaScript vanilla
- **Autenticación:** Django Auth integrado
- **Email:** SMTP (Gmail/SendGrid)
- **Estilos:** CSS personalizado con gradientes modernos

## Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Git

### Pasos de instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu_usuario/secreto-heladeria.git
cd secreto-heladeria
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

```bash
# Copiar el archivo .env.example y configurar:
cp .env.example .env
# Editar .env con tus datos reales
```

5. **Ejecutar migraciones**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**

```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**

```bash
python manage.py runserver
```

8. **Acceder al sistema**

- Sistema: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## Estructura del Proyecto

```
secreto_heladeria/
├── finanzas/              # App principal
│   ├── models.py          # Modelos: Transacción, Producto, Categoría
│   ├── views.py           # Vistas de negocio
│   ├── urls.py            # URLs de la app
│   └── admin.py           # Panel administrativo
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── dashboard.html     # Dashboard principal
│   ├── finanzas/          # Templates de finanzas
│   └── registration/      # Templates de auth
├── secreto_heladeria/     # Configuración Django
│   ├── settings.py        # Configuración principal
│   └── urls.py            # URLs principales
├── db.sqlite3             # Base de datos
├── requirements.txt       # Dependencias
├── .env                   # Variables de entorno
└── README.md              # Este archivo
```

## Diseño Visual

El sistema utiliza la **identidad visual corporativa** de Secreto Heladería:

- **Colores principales:** Rojo (#ff4757) y amarillo suave (#ffeaa7)
- **Iconografía:** Elementos de helados y repostería
- **Efectos:** Gradientes modernos, blur effects, animaciones suaves
- **Responsive:** Adaptado a dispositivos móviles
- **UX:** Interfaz intuitiva diseñada para usuarios no técnicos

## Configuración de Producción

### Variables de entorno necesarias (.env)

```bash
SECRET_KEY=tu_secret_key_real
DEBUG=False
EMAIL_HOST_USER=tu_email_real@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_real
```

### Para Gmail (App Password)

1. Activar verificación en 2 pasos
2. Generar contraseña de aplicación en Google
3. Usar esa contraseña en EMAIL_HOST_PASSWORD

## Funcionalidades Específicas

### Sistema de Usuarios

- **Superusuario:** Acceso completo al admin de Django
- **Usuarios regulares:** Acceso al sistema financiero
- **Recuperación:** Email funcional para resetear contraseñas

### Base de Datos

- Los datos del superusuario se almacenan en `db.sqlite3`
- Tablas: `auth_user`, `finanzas_transaccion`, `finanzas_producto`, `finanzas_categoria`
- Contraseñas hasheadas con algoritmos seguros de Django

### Control Financiero

- **Transacciones:** Ingresos/gastos con categorización
- **Productos:** Stock, precios, márgenes
- **Dashboard:** Métricas en tiempo real
- **Reportes:** Base para análisis futuro

## Desarrollado Para

**Secreto Heladería** - La Serena, Chile

- Heladería artesanal familiar
- Productos 100% naturales
- Enfoque en calidad y tradición
- Necesidad crítica de digitalización

## Contribución

Este proyecto fue desarrollado como solución específica para los desafíos operativos identificados en el análisis empresarial de Secreto Heladería.

## Licencia

Proyecto privado desarrollado para uso específico de Secreto Heladería.

## Soporte

Para consultas sobre implementación o configuración, contactar al desarrollador del proyecto.
