-- PRÁCTICA 1

-- Creamos la tabla departamentos 
CREATE TABLE IF NOT EXISTS departamentos (
    id                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL
);

-- Creamos la tabla empleados 
CREATE TABLE IF NOT EXISTS empleados (
    id                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    email             VARCHAR(200) UNIQUE NOT NULL,
    salario           DECIMAL(10,2),
    departamento_id   INTEGER REFERENCES departamentos(id)
);

-- Creamos la tabla proyectos 
CREATE TABLE IF NOT EXISTS proyectos (
    id                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    fecha_inicio      DATE NOT NULL,
    departamento_id   INTEGER REFERENCES departamentos(id)
);

-- Insertamos datos en la tabla departamentos
INSERT INTO departamentos 
    (nombre) 
VALUES
    ('Ventas'), 
    ('Tecnología'), 
    ('Legal'), 
    ('I+D');

-- Insertamos datos en la tabla empleados (Sara no tiene departamento)
INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

-- Insertamos datos en la tabla proyectos
-- Legal e I+D no tienen empleados
-- ni proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

-- Comprobamos que Sara no tiene departamento
SELECT *
FROM empleados
WHERE departamento_id IS NULL;

-- Hacemos un INNER JOIN de cada empleado con su departamento
-- No sale Sara porque no tiene departamento
SELECT
    empleados.nombre AS empleados,
    departamentos.nombre AS departamentos
FROM empleados
INNER JOIN departamentos ON empleados.departamento_id = departamentos.id;

-- EXTRA

-- Unimos empleados y departamentos con INNER, LEFT Y FULL OUTER JOIN, partiendo siempre de empleados

-- En el caso de INNER, saldrán empleados con departamento, es decir, 4 filas y no habrá ningún NULL.
SELECT
    empleados.nombre AS empleados,
    departamentos.nombre AS departamentos
FROM empleados
INNER JOIN departamentos ON empleados.departamento_id = departamentos.id;

-- En el caso de LEFT, saldrán todos los empleados aunque tengan o no departamento, es decir, 5 filas.
-- Habrá NULL en la columna departamentos en la fila de Sara
SELECT
    empleados.nombre AS empleados,
    departamentos.nombre AS departamentos
FROM empleados
LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id;

-- En el caso de FULL OUTER, saldrán todas las filas (7), es decir, todos los empleados tengan o no departamento
-- y todos los departamentos tengan o no empleados
-- Volverá a haber NULL en la columna departamentos en la fila de Sara
-- Habrá NULL también en la columna de empleados en las filas de departamentos Legal e I+D
SELECT
    empleados.nombre AS empleados,
    departamentos.nombre AS departamentos
FROM empleados
FULL OUTER JOIN departamentos ON empleados.departamento_id = departamentos.id;

-- Encontramos los empleados sin departamento
SELECT 
    empleados.nombre AS empleados,
    departamentos.nombre AS departamentos
FROM empleados
LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id
WHERE departamentos.id IS NULL;

-- Encontramos los departamenos sin empleado
SELECT 
    empleados.nombre AS empleados,
    departamentos.nombre AS departamentos
FROM departamentos
LEFT JOIN empleados ON empleados.departamento_id = departamentos.id
WHERE empleados.id IS NULL;

-- PRÁCTICA 2

-- Los empleados que cobran menos que la media
SELECT nombre, salario
FROM empleados
WHERE salario < (
    SELECT AVG(salario) FROM empleados
);

-- El empleado que más cobra, con MAX en la subconsulta
SELECT nombre, salario
FROM empleados
WHERE salario = (
    SELECT MAX(salario) FROM empleados
);

-- Los empleados de Tecnología, buscando su id con una subconsulta por nombre
SELECT nombre
FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos
    WHERE nombre = 'Tecnología'
);