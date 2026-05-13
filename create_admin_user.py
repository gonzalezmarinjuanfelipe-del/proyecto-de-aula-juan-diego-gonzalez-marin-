#!/usr/bin/env python3
# Script para crear usuarios admin en la BD

from flask import Flask
from flask_mysqldb import MySQL
import bcrypt
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)

def create_users():
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            
            # Contraseñas
            admin_password = "Admin123!"
            user_password = "Usuario123!"
            
            # Hash de contraseñas
            admin_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_hash = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Limpiar usuarios existentes (opcional)
            try:
                cur.execute("DELETE FROM usuarios WHERE username IN (%s, %s)", ('admin', 'usuario'))
                mysql.connection.commit()
                print("✓ Usuarios previos eliminados")
            except:
                pass
            
            # Crear usuario admin
            try:
                cur.execute("""
                    INSERT INTO usuarios (username, password_hash, nombre, email, rol)
                    VALUES (%s, %s, %s, %s, %s)
                """, ('admin', admin_hash, 'Administrador', 'admin@fetn.edu.co', 'admin'))
                mysql.connection.commit()
                print("✓ Usuario ADMIN creado")
                print(f"  Usuario: admin")
                print(f"  Contraseña: {admin_password}")
            except Exception as e:
                print(f"✗ Error al crear admin: {e}")
            
            # Crear usuario regular
            try:
                cur.execute("""
                    INSERT INTO usuarios (username, password_hash, nombre, email, rol)
                    VALUES (%s, %s, %s, %s, %s)
                """, ('usuario', user_hash, 'Usuario Prueba', 'usuario@fetn.edu.co', 'usuario'))
                mysql.connection.commit()
                print("✓ Usuario REGULAR creado")
                print(f"  Usuario: usuario")
                print(f"  Contraseña: {user_password}")
            except Exception as e:
                print(f"✗ Error al crear usuario: {e}")
            
            # Verificar usuarios creados
            cur.execute("SELECT username, nombre, rol FROM usuarios")
            usuarios = cur.fetchall()
            print(f"\n✓ Usuarios en la BD ({len(usuarios)}):")
            for u in usuarios:
                print(f"  - {u[0]} ({u[2]}) - {u[1]}")
            
            cur.close()
            print("\n✓ ¡Usuarios creados exitosamente!")
            
    except Exception as e:
        print(f"✗ Error de conexión: {str(e)}")

if __name__ == '__main__':
    create_users()
