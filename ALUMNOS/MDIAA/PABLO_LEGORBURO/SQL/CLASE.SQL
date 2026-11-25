

-- ============================================================
-- 1. CREACIÓN DE LA BASE DE DATOS Y TABLAS
-- ============================================================

CREATE TABLE departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Se añade la definición de la tabla empleados que faltaba:
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    departamento_id INT,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

CREATE TABLE proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    departamento_id INT,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

-- ============================================================
-- 2. INSERCIÓN DE DATOS
-- ============================================================

INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

INSERT INTO empleados (nombre, email, salario, departamento_id) VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

INSERT INTO proyectos (nombre, fecha_inicio, departamento_id) VALUES
    ('Web nueva',          '2026-09-01', 2),
    ('App móvil',          '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

-- ============================================================
-- 3. CONSULTAS DE TU CÓDIGO INICIAL (CORREGIDAS)
-- ============================================================

-- Consulta corregida (se añade el operador = que faltaba en nombre = 'Sara')
SELECT * 
FROM empleados
WHERE nombre = 'Sara' AND departamento_id IS NULL;

-- Consulta corregida (se cambia departamentos_id por departamento_id)
SELECT * 
FROM empleados
INNER JOIN departamentos ON empleados.departamento_id = departamentos.id;

PRACTICA 2


- Ejercicio 1: Empleados que cobran menos que la media
SELECT id, nombre, salario
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

-- Ejercicio 2: El empleado que más cobra, usando MAX en la subconsulta
SELECT id, nombre, salario
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

-- Ejercicio 3: Empleados de Tecnología mediante subconsulta por nombre
SELECT id, nombre, departamento_id
FROM empleados
WHERE departamento_id = (
    SELECT id 
    FROM departamentos 
    WHERE nombre = 'Tecnología');
    