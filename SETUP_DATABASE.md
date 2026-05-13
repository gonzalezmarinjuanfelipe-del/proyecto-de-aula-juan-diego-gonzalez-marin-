# 🔧 Guía de Configuración - Conexión a MySQL

## Pasos para conectar tu base de datos

### 1️⃣ Verifica que MySQL esté ejecutándose

- Abre **MySQL Workbench**
- Asegúrate de que tu conexión a MySQL está activa
- Nota los siguientes datos:
  - **Host**: Generalmente `localhost` o `127.0.0.1`
  - **Usuario**: Nombre de usuario (ej: `root`)
  - **Contraseña**: Tu contraseña de MySQL
  - **Puerto**: Generalmente `3306` (no editar si es por defecto)

### 2️⃣ Edita el archivo `config.py`

Abre el archivo `config.py` en este proyecto y reemplaza:

```python
MYSQL_HOST = 'localhost'      # Tu host
MYSQL_USER = 'root'           # Tu usuario
MYSQL_PASSWORD = ''           # Tu contraseña
MYSQL_DB = 'inventario_deportivo'
```

**Ejemplo real:**

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'miContraseña123'
MYSQL_DB = 'inventario_deportivo'
```

### 3️⃣ Verifica que la base de datos existe

En **MySQL Workbench**, ejecuta:

```sql
SHOW DATABASES;
```

Deberías ver `inventario_deportivo` en la lista.

Si **no existe**, ejecuta el script `database.sql`:

1. Abre MySQL Workbench
2. Ve a **File** → **Open SQL Script**
3. Selecciona `database.sql`
4. Presiona **Execute** (o Ctrl+Shift+Enter)

### 4️⃣ Prueba la conexión

Ejecuta en la terminal:

```bash
python test_db_connection.py
```

Deberías ver mensajes como:

```
✓ Conexión exitosa a MySQL versión: 8.0.30
✓ Base de datos actual: inventario_deportivo
✓ Tablas encontradas (6):
  - usuarios
  - estudiantes
  - categorias
  - implementos
  - prestamos
  - reportes
✓ Todas las pruebas completadas exitosamente!
```

### 5️⃣ ¡Inicia la aplicación!

```bash
python app.py
```

Accede a: **http://localhost:5000**

---

## 🆘 Solución de problemas

### "Access denied for user 'root'"

- Verifica que escribiste bien el usuario y contraseña en `config.py`
- Asegúrate de que MySQL está corriendo

### "Unknown database 'inventario_deportivo'"

- Ejecuta el archivo `database.sql` en MySQL Workbench

### "Can't connect to MySQL server"

- Abre MySQL Workbench y verifica que está conectado
- Asegúrate de que el host y puerto son correctos

---

## 📝 Variables de configuración adicionales

Si necesitas personalizar más, edita `config.py`:

```python
MYSQL_PORT = 3306              # Puerto de MySQL (cambiar si no es 3306)
MYSQL_CHARSET = 'utf8mb4'      # Codificación de caracteres
```

**¡Listo! Tu aplicación está lista para usarse.** 🚀
