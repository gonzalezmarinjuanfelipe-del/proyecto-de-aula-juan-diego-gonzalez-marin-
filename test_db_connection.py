#!/usr/bin/env python3
# Script para probar la conexión a MySQL

from flask import Flask
from flask_mysqldb import MySQL
import sys

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventario_deportivo'

mysql = MySQL(app)

def test_connection():
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            
            # Prueba 1: Obtener versión de MySQL
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()
            print(f"✓ Conexión exitosa a MySQL versión: {version[0]}")
            
            # Prueba 2: Verificar base de datos
            cur.execute("SELECT DATABASE()")
            db = cur.fetchone()
            print(f"✓ Base de datos actual: {db[0]}")
            
            # Prueba 3: Listar tablas
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
            print(f"✓ Tablas encontradas ({len(tables)}):")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Prueba 4: Contar registros
            cur.execute("SELECT COUNT(*) FROM usuarios")
            usuarios = cur.fetchone()[0]
            print(f"✓ Total de usuarios: {usuarios}")
            
            cur.execute("SELECT COUNT(*) FROM estudiantes")
            estudiantes = cur.fetchone()[0]
            print(f"✓ Total de estudiantes: {estudiantes}")
            
            cur.execute("SELECT COUNT(*) FROM implementos")
            implementos = cur.fetchone()[0]
            print(f"✓ Total de implementos: {implementos}")
            
            cur.close()
            
            print("\n✓ Todas las pruebas completadas exitosamente!")
            return True
            
    except Exception as e:
        print(f"✗ Error de conexión: {str(e)}", file=sys.stderr)
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
