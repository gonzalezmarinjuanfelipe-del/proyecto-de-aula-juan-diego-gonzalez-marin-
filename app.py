# app.py - Aplicación principal Flask
# Sistema de Inventario Deportivo
# Fundación Escuela Tecnológica de Neiva
# Autor: Juan Diego Gonzalez Marin

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import bcrypt
import os
from datetime import datetime, date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook
import io
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar en producción

# Configuración MySQL
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)

# Función para verificar sesión
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Ruta de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password_hash, nombre, rol FROM usuarios WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['user_id'] = user[0]
            session['user_name'] = user[2]
            session['user_role'] = user[3]
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        errors = []
        
        if not username or len(username) < 3:
            errors.append('El usuario debe tener al menos 3 caracteres')
        
        if not nombre or len(nombre) < 3:
            errors.append('El nombre debe tener al menos 3 caracteres')
        
        if not email or '@' not in email:
            errors.append('Email inválido')
        
        if not password or len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres')
        
        if password != confirm_password:
            errors.append('Las contraseñas no coinciden')
        
        if not errors:
            cur = mysql.connection.cursor()
            
            # Verificar si el usuario ya existe
            cur.execute("SELECT id FROM usuarios WHERE username = %s OR email = %s", (username, email))
            if cur.fetchone():
                errors.append('El usuario o email ya están registrados')
            
            if not errors:
                try:
                    # Hash la contraseña
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    # Insertar nuevo usuario
                    cur.execute("""
                        INSERT INTO usuarios (username, password_hash, nombre, email, rol)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (username, password_hash, nombre, email, 'usuario'))
                    mysql.connection.commit()
                    
                    flash('¡Registro exitoso! Por favor inicia sesión', 'success')
                    cur.close()
                    return redirect(url_for('login'))
                except Exception as e:
                    errors.append(f'Error al registrar: {str(e)}')
            
            cur.close()
        
        # Si hay errores, mostrarlos
        for error in errors:
            flash(error, 'error')
    
    return render_template('register.html')

# Ruta de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    
    # Estadísticas
    cur.execute("SELECT COUNT(*) FROM implementos")
    total_implementos = cur.fetchone()[0]
    
    cur.execute("SELECT SUM(cantidad_total - cantidad_disponible) FROM implementos")
    implementos_prestados = cur.fetchone()[0] or 0
    
    cur.execute("SELECT COUNT(*) FROM estudiantes")
    total_estudiantes = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM implementos WHERE cantidad_disponible < 5")
    stock_bajo = cur.fetchone()[0]
    
    # Actividad reciente
    cur.execute("""
        SELECT p.fecha_prestamo, e.nombre, i.nombre, p.cantidad_prestada
        FROM prestamos p
        JOIN estudiantes e ON p.estudiante_id = e.id
        JOIN implementos i ON p.implemento_id = i.id
        ORDER BY p.fecha_prestamo DESC LIMIT 5
    """)
    actividad_reciente = cur.fetchall()
    
    cur.close()
    
    return render_template('dashboard.html', 
                         total_implementos=total_implementos,
                         implementos_prestados=implementos_prestados,
                         total_estudiantes=total_estudiantes,
                         stock_bajo=stock_bajo,
                         actividad_reciente=actividad_reciente)

# Inventario
@app.route('/inventario')
@login_required
def inventario():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT i.id, i.nombre, c.nombre, i.cantidad_total, i.cantidad_disponible, i.estado, i.descripcion
        FROM implementos i
        LEFT JOIN categorias c ON i.categoria_id = c.id
    """)
    implementos = cur.fetchall()
    cur.close()
    return render_template('inventario.html', implementos=implementos)

# Agregar implemento
@app.route('/agregar_implemento', methods=['GET', 'POST'])
@login_required
def agregar_implemento():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria_id = request.form['categoria_id']
        cantidad_total = request.form['cantidad_total']
        descripcion = request.form['descripcion']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO implementos (nombre, categoria_id, cantidad_total, cantidad_disponible, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, categoria_id, cantidad_total, cantidad_total, descripcion))
        mysql.connection.commit()
        cur.close()
        
        flash('Implemento agregado exitosamente', 'success')
        return redirect(url_for('inventario'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM categorias")
    categorias = cur.fetchall()
    cur.close()
    
    return render_template('agregar_implemento.html', categorias=categorias)

# Editar implemento
@app.route('/editar_implemento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_implemento(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria_id = request.form['categoria_id']
        cantidad_total = request.form['cantidad_total']
        descripcion = request.form['descripcion']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE implementos SET nombre=%s, categoria_id=%s, cantidad_total=%s, descripcion=%s
            WHERE id=%s
        """, (nombre, categoria_id, cantidad_total, descripcion, id))
        mysql.connection.commit()
        cur.close()
        
        flash('Implemento actualizado exitosamente', 'success')
        return redirect(url_for('inventario'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM implementos WHERE id = %s", (id,))
    implemento = cur.fetchone()
    cur.execute("SELECT id, nombre FROM categorias")
    categorias = cur.fetchall()
    cur.close()
    
    return render_template('editar_implemento.html', implemento=implemento, categorias=categorias)

# Eliminar implemento
@app.route('/eliminar_implemento/<int:id>')
@login_required
def eliminar_implemento(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM implementos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Implemento eliminado exitosamente', 'success')
    return redirect(url_for('inventario'))

# Estudiantes
@app.route('/estudiantes')
@login_required
def estudiantes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM estudiantes")
    estudiantes = cur.fetchall()
    cur.close()
    return render_template('estudiantes.html', estudiantes=estudiantes)

# Agregar estudiante
@app.route('/agregar_estudiante', methods=['GET', 'POST'])
@login_required
def agregar_estudiante():
    if request.method == 'POST':
        codigo = request.form['codigo_estudiantil']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        carrera = request.form['carrera']
        semestre = request.form['semestre']
        telefono = request.form['telefono']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO estudiantes (codigo_estudiantil, nombre, apellido, carrera, semestre, telefono, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (codigo, nombre, apellido, carrera, semestre, telefono, email))
        mysql.connection.commit()
        cur.close()
        
        flash('Estudiante agregado exitosamente', 'success')
        return redirect(url_for('estudiantes'))
    
    return render_template('agregar_estudiante.html')

# Préstamos
@app.route('/prestamos')
@login_required
def prestamos():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, e.nombre, e.apellido, i.nombre, p.cantidad_prestada, p.fecha_prestamo, 
               p.fecha_devolucion_esperada, p.estado
        FROM prestamos p
        JOIN estudiantes e ON p.estudiante_id = e.id
        JOIN implementos i ON p.implemento_id = i.id
        ORDER BY p.fecha_prestamo DESC
    """)
    prestamos = cur.fetchall()
    cur.close()
    return render_template('prestamos.html', prestamos=prestamos)

# Registrar préstamo
@app.route('/registrar_prestamo', methods=['GET', 'POST'])
@login_required
def registrar_prestamo():
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        implemento_id = request.form['implemento_id']
        cantidad = request.form['cantidad']
        fecha_devolucion = request.form['fecha_devolucion']
        
        cur = mysql.connection.cursor()
        
        # Verificar stock disponible
        cur.execute("SELECT cantidad_disponible FROM implementos WHERE id = %s", (implemento_id,))
        disponible = cur.fetchone()[0]
        
        if int(cantidad) > disponible:
            flash('No hay suficiente stock disponible', 'error')
            cur.close()
            return redirect(url_for('registrar_prestamo'))
        
        # Registrar préstamo
        cur.execute("""
            INSERT INTO prestamos (estudiante_id, implemento_id, cantidad_prestada, fecha_devolucion_esperada, usuario_registro)
            VALUES (%s, %s, %s, %s, %s)
        """, (estudiante_id, implemento_id, cantidad, fecha_devolucion, session['user_id']))
        
        # Actualizar stock
        cur.execute("""
            UPDATE implementos SET cantidad_disponible = cantidad_disponible - %s WHERE id = %s
        """, (cantidad, implemento_id))
        
        mysql.connection.commit()
        cur.close()
        
        flash('Préstamo registrado exitosamente', 'success')
        return redirect(url_for('prestamos'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, CONCAT(nombre, ' ', apellido) FROM estudiantes")
    estudiantes = cur.fetchall()
    cur.execute("SELECT id, nombre FROM implementos WHERE cantidad_disponible > 0")
    implementos = cur.fetchall()
    cur.close()
    
    return render_template('registrar_prestamo.html', estudiantes=estudiantes, implementos=implementos)

# Devolver préstamo
@app.route('/devolver_prestamo/<int:id>')
@login_required
def devolver_prestamo(id):
    cur = mysql.connection.cursor()
    
    # Obtener información del préstamo
    cur.execute("SELECT implemento_id, cantidad_prestada FROM prestamos WHERE id = %s", (id,))
    prestamo = cur.fetchone()
    
    # Actualizar préstamo
    cur.execute("""
        UPDATE prestamos SET estado='devuelto', fecha_devolucion_real=%s WHERE id=%s
    """, (date.today(), id))
    
    # Actualizar stock
    cur.execute("""
        UPDATE implementos SET cantidad_disponible = cantidad_disponible + %s WHERE id = %s
    """, (prestamo[1], prestamo[0]))
    
    mysql.connection.commit()
    cur.close()
    
    flash('Préstamo devuelto exitosamente', 'success')
    return redirect(url_for('prestamos'))

# Reportes
@app.route('/reportes')
@login_required
def reportes():
    return render_template('reportes.html')

# Generar reporte PDF
@app.route('/generar_reporte_pdf')
@login_required
def generar_reporte_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Reporte de Inventario Deportivo")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 70, "Fundación Escuela Tecnológica de Neiva")
    p.drawString(100, height - 90, f"Generado por: {session['user_name']}")
    p.drawString(100, height - 110, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Contenido
    y = height - 150
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre, cantidad_total, cantidad_disponible FROM implementos")
    implementos = cur.fetchall()
    cur.close()
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Implemento")
    p.drawString(250, y, "Total")
    p.drawString(350, y, "Disponible")
    y -= 20
    
    p.setFont("Helvetica", 10)
    for imp in implementos:
        p.drawString(50, y, str(imp[0]))
        p.drawString(250, y, str(imp[1]))
        p.drawString(350, y, str(imp[2]))
        y -= 15
    
    p.save()
    buffer.seek(0)
    
    response = app.response_class(buffer.getvalue(), mimetype='application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='reporte_inventario.pdf')
    return response

if __name__ == '__main__':
    app.run(debug=True)