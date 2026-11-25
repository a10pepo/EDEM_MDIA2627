-- =======================================================
-- PRÁCTICA 1: CREACIÓN DE TABLAS, CARGA DE DATOS Y JOINS
-- =======================================================

-- 'departamentos' se crea primero porque es la tabla del lado "1" de la relación
-- (la tabla referenciada). Las tablas con FOREIGN KEY no pueden crearse antes.

DROP TABLE IF EXISTS proyectos;
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS departamentos;

CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla empleados con foreign key a departamentos
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    salario NUMERIC(10, 2) NOT NULL,
    departamento_id INT,
    CONSTRAINT fk_empleados_departamento
        FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

-- Tabla proyectos con foreign key a departamentos
CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento_id INT,
    CONSTRAINT fk_proyectos_departamento
        FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

-- Inserción de datos
INSERT INTO departamentos (id, nombre) VALUES
(1, 'Tecnología'),
(2, 'Marketing'),
(3, 'Ventas');

-- Salarios de ejemplo para practicar las subconsultas de la práctica 2.
-- Sara no tiene departamento asignado (NULL).
INSERT INTO empleados (id, nombre, salario, departamento_id) VALUES
(1, 'Carlos', 50000, 1),
(2, 'Ana', 52000, 1),
(3, 'Luis', 38000, 2),
(4, 'Marta', 45000, 3),
(5, 'Sara', 29000, NULL);

-- Proyectos
INSERT INTO proyectos (id, nombre, departamento_id) VALUES
(1, 'Nueva Web', 1),
(2, 'Campaña Redes', 2),
(3, 'Migración Cloud', 1);

-- Comprobar que Sara no tiene departamento
SELECT departamento_id
FROM empleados
WHERE nombre = 'Sara';

-- INNER JOIN de cada empleado con su departamento (¿Quién no sale? -> Sara)
SELECT 
    e.id AS empleado_id,
    e.nombre AS empleado_nombre,
    d.id AS departamento_id,
    d.nombre AS departamento_nombre
FROM empleados e
INNER JOIN departamentos d 
    ON e.departamento_id = d.id;

-- LEFT JOIN para localizar los empleados sin departamento asignado (Sara)
SELECT
    e.id AS empleado_id,
    e.nombre AS empleado_nombre,
    e.departamento_id,
    d.nombre AS departamento_nombre
FROM empleados e
LEFT JOIN departamentos d
    ON e.departamento_id = d.id
WHERE e.departamento_id IS NULL;
