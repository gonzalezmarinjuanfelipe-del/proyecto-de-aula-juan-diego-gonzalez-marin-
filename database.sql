-- Base de datos para Sistema de Inventario Deportivo
-- Fundación Escuela Tecnológica de Neiva
-- Autor: Juan Diego Gonzalez Marin

CREATE DATABASE IF NOT EXISTS inventario_deportivo;
USE inventario_deportivo;

-- Tabla de usuarios/administradores
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rol ENUM('admin', 'usuario') DEFAULT 'usuario',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de estudiantes
CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_estudiantil VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    semestre INT NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de categorías de implementos
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Tabla de implementos deportivos
CREATE TABLE implementos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria_id INT,
    cantidad_total INT NOT NULL DEFAULT 0,
    cantidad_disponible INT NOT NULL DEFAULT 0,
    estado ENUM('disponible', 'prestado', 'dañado', 'mantenimiento') DEFAULT 'disponible',
    descripcion TEXT,
    imagen VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Tabla de préstamos
CREATE TABLE prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    implemento_id INT NOT NULL,
    cantidad_prestada INT NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE NULL,
    estado ENUM('activo', 'devuelto', 'vencido') DEFAULT 'activo',
    observaciones TEXT,
    usuario_registro INT,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (implemento_id) REFERENCES implementos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_registro) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Insertar usuario administrador por defecto
INSERT INTO usuarios (username, password_hash, nombre, email, rol) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fCwHn/7a', 'Administrador', 'admin@etn.edu.co', 'admin');

-- Insertar categorías de ejemplo
INSERT INTO categorias (nombre, descripcion) VALUES
('Baloncesto', 'Implementos para baloncesto'),
('Fútbol', 'Implementos para fútbol'),
('Voleibol', 'Implementos para voleibol'),
('Atletismo', 'Implementos para atletismo'),
('Natación', 'Implementos para natación');

-- Insertar implementos de ejemplo
INSERT INTO implementos (nombre, categoria_id, cantidad_total, cantidad_disponible, descripcion) VALUES
('Balón de Baloncesto', 1, 10, 10, 'Balón oficial de baloncesto'),
('Balón de Fútbol', 2, 15, 15, 'Balón de fútbol tamaño 5'),
('Red de Voleibol', 3, 5, 5, 'Red completa para voleibol'),
('Conos de Atletismo', 4, 20, 20, 'Conos plásticos para entrenamiento'),
('Gafas de Natación', 5, 12, 12, 'Gafas protectoras para natación');