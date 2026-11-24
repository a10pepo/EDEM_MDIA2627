--ENTREGABLE SQL
--PRACTICA 1
CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR (100) NOT NULL 
);

DROP TABLE deepartamentos;

CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    salario INTEGER NOT NULL, 
    departamento_id INTEGER REFERENCES departamentos(id)
);

CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    departamento_id INTEGER NOT NULL REFERENCES departamentos(id)
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

SELECT * FROM empleados;
SELECT * FROM proyectos;
SELECT * FROM departamentos;

SELECT 
    empleados.nombre, 
    empleados.departamento_id,
    departamentos.nombre as nombre_departamento
FROM  empleados
INNER JOIN departamentos ON departamentos.id = empleados.departamento_id;

SELECT 
    empleados.nombre, 
    empleados.departamento_id
FROM  empleados
LEFT JOIN departamentos ON departamentos.id = empleados.departamento_id
WHERE departamento_id IS NULL;

--PRACTICA 2
SELECT nombre, salario
FROM empleados
WHERE salario < (
    SELECT AVG(salario)
    FROM empleados
);

SELECT nombre, salario
FROM empleados
WHERE salario = (
    SELECT MAX(salario)
    FROM empleados
);

SELECT nombre
FROM empleados
WHERE departamento_id IN (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);