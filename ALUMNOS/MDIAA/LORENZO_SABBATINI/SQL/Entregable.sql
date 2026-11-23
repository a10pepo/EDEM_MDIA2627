# Practica 1

CREATE TABLE departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

CREATE TABLE empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    email VARCHAR(50),
    salario INTEGER,
    departamento_id INTEGER REFERENCES departamentos(id)
);

CREATE TABLE proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
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
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

-- Comprueba que Sara no tiene departamento.
SELECT 
    departamentos.nombre AS Departamento, 
    empleados.nombre AS Nombre
FROM empleados
LEFT JOIN departamentos ON departamentos.id = empleados.departamento_id
WHERE empleados.departamento_id IS NULL;

-- Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale?
SELECT 
    departamentos.nombre AS Departamento, 
    empleados.nombre AS Nombre
FROM empleados
INNER JOIN departamentos ON departamentos.id = empleados.departamento_id

-----

# Practica 2

-- Los empleados que cobran menos que la media.
SELECT nombre, salario
FROM empleados
WHERE salario < (
    SELECT AVG(salario) FROM empleados
    );

-- El empleado que más cobra, con MAX en la subconsulta.
SELECT nombre, salario
FROM empleados
WHERE salario = (
    SELECT MAX(salario) FROM empleados
    );

-- Los empleados de Tecnología, buscando su id con una subconsulta por nombre.
SELECT nombre
FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);
