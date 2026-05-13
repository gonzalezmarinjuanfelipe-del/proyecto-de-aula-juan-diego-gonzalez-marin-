# Sistema de Inventario Deportivo

## Fundación Escuela Tecnológica de Neiva

**Autor:** Juan Diego Gonzalez Marin

Un sistema web completo y profesional para la gestión del inventario de útiles deportivos de la institución universitaria.

## 🚀 Características

### ✨ Funcionalidades Principales

- **Dashboard Administrativo** con estadísticas en tiempo real
- **Gestión de Inventario** completo (agregar, editar, eliminar implementos)
- **Gestión de Estudiantes** con información detallada
- **Sistema de Préstamos** con control de stock automático
- **Reportes Profesionales** en PDF y Excel
- **Interfaz Moderna** con diseño universitario premium

### 🎨 Diseño y UX

- **Interfaz Universitaria** elegante y moderna
- **Glassmorphism** y efectos visuales avanzados
- **Responsive Design** perfecto en todos los dispositivos
- **Animaciones Suaves** y microinteracciones
- **Paleta de Colores** institucional azul y cyan
- **Modo Oscuro/Claro** próximamente

### 🔒 Seguridad

- **Autenticación Segura** con hash de contraseñas
- **Validaciones Backend** completas
- **Protección SQL Injection**
- **Sesiones Seguras** y manejo de errores
- **Roles de Usuario** (admin/usuario)

## 🛠️ Tecnologías Utilizadas

### Backend

- **Python Flask** - Framework web robusto
- **MySQL** - Base de datos relacional
- **bcrypt** - Encriptación de contraseñas

### Frontend

- **HTML5** - Estructura semántica
- **CSS3** - Estilos modernos con variables CSS
- **JavaScript** - Interactividad y animaciones
- **Bootstrap 5** - Framework CSS responsive
- **Chart.js** - Gráficos interactivos
- **Font Awesome** - Iconografía profesional

### Arquitectura

- **MVC** - Patrón de arquitectura
- **RESTful API** - Endpoints bien estructurados
- **Modular** - Código organizado y escalable

## 📋 Requisitos del Sistema

- Python 3.8+
- MySQL 5.7+
- Navegador web moderno
- Conexión a internet (para CDN de Bootstrap/Font Awesome)

## Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/inventario-deportivo.git
cd inventario-deportivo
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos MySQL

#### Crear Base de Datos

```sql
CREATE DATABASE inventario_deportivo;
```

#### Ejecutar Script SQL

```bash
mysql -u root -p inventario_deportivo < database.sql
```

#### Configurar Conexión

Editar `app.py` con tus credenciales de MySQL:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tu_usuario'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña'
app.config['MYSQL_DB'] = 'inventario_deportivo'
```

### 5. Ejecutar la Aplicación

```bash
python app.py
```

### 6. Acceder al Sistema

- Abrir navegador en: `http://localhost:5000`
- Usuario por defecto: `admin`
- Contraseña por defecto: `admin123`

## Estructura del Proyecto

```
inventario-deportivo/
├── app.py                      # Aplicación principal Flask
├── database.sql                # Script de base de datos
├── requirements.txt            # Dependencias Python
├── README.md                   # Documentación
├── static/
│   ├── css/
│   │   └── styles.css         # Estilos CSS principales
│   ├── js/
│   │   ├── login.js           # Funcionalidades del login
│   │   ├── main.js            # Funciones generales
│   │   └── dashboard.js       # Dashboard interactivo
│   └── images/                 # Imágenes del sistema
└── templates/
    ├── login.html              # Página de login
    ├── dashboard.html          # Dashboard principal
    ├── inventario.html         # Gestión de inventario
    ├── agregar_implemento.html # Formulario agregar implemento
    ├── editar_implemento.html  # Formulario editar implemento
    ├── estudiantes.html        # Lista de estudiantes
    ├── agregar_estudiante.html # Formulario agregar estudiante
    ├── prestamos.html          # Gestión de préstamos
    ├── registrar_prestamo.html # Formulario registrar préstamo
    └── reportes.html           # Sistema de reportes
```

## Base de Datos

### Tablas Principales

- **usuarios** - Administradores del sistema
- **estudiantes** - Información de estudiantes
- **categorias** - Categorías de implementos
- **implementos** - Inventario de útiles deportivos
- **prestamos** - Registro de préstamos

### Relaciones

- Un estudiante puede tener múltiples préstamos
- Un implemento pertenece a una categoría
- Un préstamo registra usuario que lo creó

## Uso del Sistema

### Dashboard

- Visualiza estadísticas generales
- Gráficos de distribución por categorías
- Actividad reciente del sistema

### Inventario

- Agregar nuevos implementos con categorías
- Editar información existente
- Eliminar implementos no utilizados
- Control automático de stock

### Estudiantes

- Registrar nuevos estudiantes
- Gestionar información académica
- Historial de préstamos por estudiante

### Préstamos

- Registrar nuevos préstamos
- Validación automática de stock disponible
- Devolución con actualización de inventario
- Historial completo de movimientos

### Reportes

- Generar reportes PDF profesionales
- Exportar datos a Excel
- Información detallada del inventario

## Configuración Avanzada

### Variables de Entorno

Crear archivo `.env`:

```
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_muy_segura
MYSQL_HOST=localhost
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=inventario_deportivo
```

### Ejecutar en Modo Producción

```bash
export FLASK_ENV=production
python app.py
```

## Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver archivo [LICENSE](LICENSE) para más detalles.

## Contacto

**Juan Diego Gonzalez Marin**

- Email: juan.diego@email.com
- LinkedIn: [Juan Diego Gonzalez](https://linkedin.com/in/juandiegogonzalez)
- GitHub: [juandiegogonzalez](https://github.com/juandiegogonzalez)

## 🙏 Agradecimientos

- Fundación Escuela Tecnológica de Neiva
- Comunidad de desarrollo Flask
- Bootstrap y Font Awesome por sus excelentes frameworks

---

**Desarrollado con ❤️ para la comunidad universitaria**
