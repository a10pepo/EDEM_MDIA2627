
-- PRACTICA 1 --
CREATE DATABASE entregable_SQL;

CREATE TABLE IF NOT EXISTS departamentos (
    id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR (50)
)

CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50),
    email TEXT UNIQUE NOT NULL,
    salario NUMERIC(8,2),
    departamento_id INTEGER REFERENCES departamentos(id)
)

CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50),
    fecha_inicio DATE,
    departamento_id INTEGER REFERENCES departamentos(id)  
)

-- Departamentos
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

SELECT * FROM departamentos;
-- Empleados (Sara no tiene departamento)
INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

SELECT * FROM empleados;

INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

SELECT * FROM proyectos;

SELECT empleados.nombre AS nombre_empleado, departamentos.nombre AS nombre_departamento FROM empleados LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id WHERE empleados.departamento_id IS NULL;

SELECT empleados.nombre AS nombre_empleado, departamentos.nombre AS nombre_departamento FROM empleados INNER JOIN departamentos ON departamentos.id = empleados.departamento_id;


-- EXTRA --
SELECT * FROM empleados INNER JOIN departamentos ON empleados.departamento_id = departamentos.id;
SELECT * FROM empleados LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id;
SELECT * FROM empleados FULL OUTER JOIN departamentos ON empleados.departamento_id = departamentos.id;

SELECT empleados.nombre AS nombre_empleado, departamentos.nombre AS nombre_departamento FROM empleados LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id WHERE empleados.departamento_id IS NULL;
SELECT departamentos.nombre AS nombre_departamento, empleados.nombre AS nombre_empleado FROM departamentos LEFT JOIN empleados ON departamentos.id = empleados.departamento_id WHERE empleados.departamento_id IS NULL;


-- PRACTICA 2 --

SELECT * FROM empleados WHERE salario < (SELECT AVG(salario) FROM empleados);
SELECT * FROM empleados WHERE salario = (SELECT MAX(salario) FROM empleados);
--SELECT nombre FROM empleados WHERE nombre IN (SELECT empleados.nombre FROM empleados LEFT JOIN departamentos ON departamentos.id = empleados.departamento_id WHERE departamentos.nombre = 'Tecnología')
SELECT * FROM empleados WHERE departamento_id IN (SELECT id FROM departamentos WHERE nombre LIKE 'Tecnología');

