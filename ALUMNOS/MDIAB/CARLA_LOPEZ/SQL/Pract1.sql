CREATE DATABASE Entregable_SQL;

-- Tabla departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR NOT NULL
);

-- Tabla empleados
CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    email VARCHAR,
    salario NUMERIC,
    departamento_id INTEGER REFERENCES departamentos(id)
);

-- Tabla proyectos
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    fecha_inicio DATE,
    departamento_id INTEGER REFERENCES departamentos(id)
);

-- Departamentos
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

-- Empleados (Sara no tiene departamento)
INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

-- Proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',        '2026-09-01', 2),
    ('App móvil',        '2026-11-15', 2),
    ('Campaña de verano','2027-05-01', 1);

-- Legal e I+D no tienen empleados
-- ni proyectos


SELECT * FROM departamentos;
SELECT * FROM empleados;
SELECT * FROM proyectos;

-- Para ver si Sara tiene departamento
SELECT *
FROM empleados
WHERE departamento_id IS NULL;

-- Inner Join con cada empleado
SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id;


-- Left Join para ver quien falta
SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM empleados
LEFT JOIN departamentos
ON empleados.departamento_id = departamentos.id;
-- Falta Sara.

-- EXTRA 1 y 2
SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM empleados
INNER JOIN departamentos 
ON empleados.departamento_id = departamentos.id;

SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM empleados
LEFT JOIN departamentos 
ON empleados.departamento_id = departamentos.id;

SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM empleados
FULL OUTER JOIN departamentos 
ON empleados.departamento_id = departamentos.id;

-- Extra 3
SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM empleados
FULL OUTER JOIN departamentos
ON empleados.departamento_id = departamentos.id
WHERE empleados.id IS NULL OR departamentos.id IS NULL;