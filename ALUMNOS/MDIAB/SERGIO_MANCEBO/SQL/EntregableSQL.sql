-- ************************
--      PRÁCTICA 1
-- ************************

-- 1. Tabla Departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    id                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL UNIQUE
);
SELECT * FROM departamentos;
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');


-- 2. Tabla Empleados
CREATE TABLE IF NOT EXISTS empleados (
    id                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    email             VARCHAR(200) UNIQUE,
    salario           INTEGER,
    departamento_id   BIGINT REFERENCES departamentos(id)
);

INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

-- 3. Tabla Proyectos
CREATE TABLE IF NOT EXISTS proyectos (
    id                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    fecha_inicio      DATE,
    departamento_id   BIGINT REFERENCES departamentos(id)
);

INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

-- COMPRUEBA QUE SARA NO TIENE DEPARTAMENTO
SELECT nombre AS EMPLEADO,
       departamento_id AS DEPARTAMENTO
FROM empleados 
WHERE departamento_id IS NULL

-- INNER JOIN DE CADA EMPLEADO CON SU DEPARTAMENTO
SELECT empleados.nombre AS EMPLEADO,
       departamentos.nombre AS DEPARTAMENTO
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id;

-- ¿Quién no sale?
--      Empleada: Sara
--      Departamentos: Legal ; I+D
SELECT 
    empleados.nombre AS empleado, 
    departamentos.nombre AS departamento
FROM empleados
FULL OUTER JOIN departamentos ON empleados.departamento_id = departamentos.id
WHERE empleados.nombre IS NULL OR departamentos.nombre IS NULL;


-- ************************
--      PRÁCTICA 2
-- ************************

-- LOS EMPLEADOS QUE COBRAN MENOS QUE LA MEDIA
SELECT nombre, salario
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

-- EL EMPLEADO QUE MÁS COBRA, CON MAX EN LA SUBCONSULTA
SELECT nombre, salario
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

-- LOS EMPLEADOS DE 'Tecnología', BUSCANDO SU ID CON UNA SUBCONSULTA POR NOMBRE
SELECT nombre, email
FROM empleados
WHERE departamento_id = (
    SELECT id 
    FROM departamentos 
    WHERE nombre = 'Tecnología'
);