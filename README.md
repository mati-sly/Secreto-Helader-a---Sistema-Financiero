# 🍦 Secreto Heladería - Sistema de Gestión Financiera

Sistema de gestión financiera desarrollado específicamente para **Secreto Heladería**, una heladería artesanal ubicada en La Serena, Chile.

## 📋 Tabla de Contenidos

- [Contexto del Proyecto](#contexto-del-proyecto)
- [Características Principales](#características-principales)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso del Sistema](#uso-del-sistema)
- [Datos de Ejemplo](#datos-de-ejemplo)
- [Despliegue en Producción](#despliegue-en-producción)
- [Contribución](#contribución)

## 📊 Contexto del Proyecto

Este sistema fue desarrollado para solucionar la **crisis de gestión manual** identificada en el análisis empresarial de Secreto Heladería:

### 🔴 Problemas Identificados
- Gestión 100% manual con cuadernos físicos
- Ausencia de control financiero digital  
- Sin seguimiento de inventario automatizado
- Estacionalidad extrema que requiere análisis de datos
- Falta de sistemas profesionales básicos

### 💡 Solución Implementada
Sistema web integral que digitaliza todas las operaciones financieras y de inventario, proporcionando análisis en tiempo real y reportes automatizados.

## ✨ Características Principales

### 🔐 Sistema de Autenticación
- Login seguro con diseño corporativo
- Recuperación de contraseña funcional via email
- Sistema de permisos multinivel
- Redirecciones automáticas según rol

### 💰 Control Financiero
- **Dashboard en tiempo real** con métricas del día
- Registro de ingresos y gastos categorizados
- Transacciones detalladas (fecha, monto, descripción)
- **Cálculo automático de utilidades y márgenes**
- Reportes históricos y análisis de tendencias

### 🛍️ Gestión de Productos e Inventario
- Catálogo completo con categorización
- Control de stock con **alertas de inventario bajo**
- Gestión de precios y márgenes de ganancia
- Categorías: Helados, Café, Pastelería, Otros

### 📈 Reportes y Análisis
- Estadísticas diarias automáticas
- Historial filtrable de transacciones
- Análisis de productos más vendidos
- **Preparado para expansión** con gráficos avanzados

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnología |
|-----------|------------|
| **Backend** | Django 4.2+ (Python) |
| **Base de Datos** | SQLite3 (desarrollo) / PostgreSQL (producción) |
| **Frontend** | HTML5, CSS3, JavaScript ES6 |
| **Autenticación** | Django Authentication System |
| **Email** | SMTP (Gmail/SendGrid) |
| **Estilos** | CSS personalizado con gradientes corporativos |

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu_usuario/secreto-heladeria.git
   cd secreto-heladeria
   ```

2. **Crear y activar entorno virtual**
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # Activar entorno virtual
   # En Linux/Mac:
   source venv/bin/activate
   # En Windows:
   venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones de base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear usuario administrador**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

7. **Acceder al sistema**
   - **Sistema principal:** http://127.0.0.1:8000
   - **Panel administrativo:** http://127.0.0.1:8000/admin

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de Django
SECRET_KEY=tu_secret_key_muy_segura_aqui
DEBUG=True

# Configuración de Email (Gmail)
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_de_gmail

# Base de datos (opcional para producción)
DATABASE_URL=postgresql://usuario:password@localhost/secreto_heladeria
```

### Configuración de Email para Recuperación de Contraseña

Para usar Gmail:

1. Activar **verificación en 2 pasos** en tu cuenta de Google
2. Generar una **contraseña de aplicación** en la configuración de seguridad
3. Usar esa contraseña en `EMAIL_HOST_PASSWORD`

## 📁 Estructura del Proyecto

```
secreto_heladeria/
├── 📂 finanzas/                    # Aplicación principal
│   ├── 📄 models.py                # Modelos de datos
│   ├── 📄 views.py                 # Lógica de negocio
│   ├── 📄 urls.py                  # Rutas de la aplicación
│   ├── 📄 admin.py                 # Panel administrativo
│   └── 📂 migrations/              # Migraciones de BD
├── 📂 templates/                   # Plantillas HTML
│   ├── 📄 base.html                # Plantilla base
│   ├── 📄 dashboard.html           # Panel principal
│   ├── 📂 finanzas/                # Plantillas de finanzas
│   └── 📂 registration/            # Plantillas de autenticación
├── 📂 static/                      # Archivos estáticos
│   ├── 📂 css/                     # Hojas de estilo
│   ├── 📂 js/                      # JavaScript
│   └── 📂 img/                     # Imágenes
├── 📂 secreto_heladeria/           # Configuración Django
│   ├── 📄 settings.py              # Configuración principal
│   ├── 📄 urls.py                  # URLs principales
│   └── 📄 wsgi.py                  # WSGI config
├── 📄 db.sqlite3                   # Base de datos SQLite
├── 📄 requirements.txt             # Dependencias Python
├── 📄 .env                         # Variables de entorno
└── 📄 README.md                    # Este archivo
```

## 📱 Uso del Sistema

### Panel Principal (Dashboard)
- **Resumen diario:** Ingresos, gastos y utilidad del día
- **Métricas rápidas:** Total de productos, alertas de stock
- **Accesos directos:** A todas las funcionalidades principales

### Gestión de Transacciones
- **Registrar ingresos:** Ventas por categoría de producto
- **Registrar gastos:** Compras, servicios, mantenimiento
- **Historial:** Filtros por fecha, categoría y tipo

### Control de Inventario
- **Productos:** Agregar, editar, eliminar productos
- **Stock:** Control automático con alertas
- **Categorías:** Organización por tipo de producto

## 🌱 Datos de Ejemplo

Para poblar la base de datos con datos de ejemplo, ejecuta:

```bash
# Cargar categorías y productos
python manage.py loaddata 00_catalogo_categoria_producto_es.json

# Cargar transacciones de ejemplo
python manage.py loaddata 00_catalogo_transacciones.json
```

### Comandos Personalizados (si están disponibles)
```bash
# Exportar datos actuales
python manage.py seed_export

# Importar datos desde JSON
python manage.py seed_import
```

## 🚀 Despliegue en Producción

### Variables de Entorno para Producción

```env
SECRET_KEY=tu_secret_key_real_muy_segura
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://usuario:password@servidor/base_datos
EMAIL_HOST_USER=noreply@tudominio.com
EMAIL_HOST_PASSWORD=tu_password_smtp
```

### Consideraciones de Seguridad

- Usar HTTPS en producción
- Configurar firewall apropiado
- Backup regular de base de datos
- Monitoreo de logs de acceso

## 🎨 Diseño Visual

El sistema implementa la **identidad visual corporativa** de Secreto Heladería:

- **Colores principales:** Rojo vibrante (#ff4757) y amarillo suave (#ffeaa7)
- **Tipografía:** Fuentes modernas y legibles
- **Efectos visuales:** Gradientes, sombras sutiles y animaciones fluidas
- **Responsive design:** Optimizado para dispositivos móviles y tablets
- **UX/UI:** Interfaz intuitiva diseñada para usuarios no técnicos

## 👥 Usuarios y Permisos

### Tipos de Usuario
- **Superusuario:** Acceso completo al admin de Django
- **Staff:** Acceso al sistema financiero completo
- **Usuario regular:** Acceso limitado a consultas

### Funcionalidades por Rol
| Funcionalidad | Superusuario | Staff | Usuario |
|---------------|--------------|-------|---------|
| Dashboard | ✅ | ✅ | ✅ |
| Registrar transacciones | ✅ | ✅ | ❌ |
| Gestionar productos | ✅ | ✅ | ❌ |
| Ver reportes | ✅ | ✅ | ✅ |
| Admin Django | ✅ | ❌ | ❌ |

## 🏢 Desarrollado Para

**Secreto Heladería** - La Serena, Chile

- Heladería artesanal familiar con más de 10 años de tradición
- Productos 100% naturales y elaboración propia
- Enfoque en calidad, tradición e innovación
- Necesidad crítica de digitalización para optimizar operaciones

## 🤝 Contribución

Este proyecto fue desarrollado como solución específica para los desafíos operativos de Secreto Heladería, basándose en:

- Análisis exhaustivo de procesos actuales
- Entrevistas con propietarios y empleados
- Evaluación de necesidades específicas del negocio
- Diseño centrado en el usuario final

### Para Contribuir
1. Fork del repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Proyecto desarrollado específicamente para **Secreto Heladería**. Todos los derechos reservados.

## 🆘 Soporte

Para consultas sobre implementación, configuración o nuevas funcionalidades:

- **Email:** soporte@secreto-heladeria.cl
- **Documentación:** Ver wiki del proyecto
- **Issues:** Usar el sistema de issues de GitHub

---

> **Nota:** Este sistema ha transformado la gestión de Secreto Heladería, eliminando el trabajo manual y proporcionando insights valiosos para la toma de decisiones empresariales.

**Desarrollado con ❤️ para Secreto Heladería - La Serena, Chile**
