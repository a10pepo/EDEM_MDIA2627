CREATE TABLE IF NOT EXISTS departamentos (
    id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  VARCHAR (100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS empleados (
    id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL,
    email   VARCHAR(250) NOT NULL UNIQUE,
    salario NUMERIC(10,2) NOT NULL,
    departamento_id INTEGER REFERENCES departamentos(id)
);

CREATE TABLE IF NOT EXISTS proyectos (
    id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
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

SELECT nombre
FROM empleados
WHERE departamento_id IS NULL;

SELECT departamentos.nombre AS nombre_dpto, empleados.nombre AS nombre FROM empleados
INNER JOIN departamentos ON empleados.departamento_id = departamentos.id;

SELECT nombre, salario
FROM empleados
WHERE salario < (SELECT avg(salario) from empleados);

SELECT nombre, salario
FROM empleados
WHERE salario = (SELECT max(salario) from empleados);

SELECT id 
FROM departamentos
WHERE nombre = 'Tecnología'

SELECT nombre
FROM empleados
WHERE departamento_id IN (
    SELECT id 
FROM departamentos
WHERE nombre = 'Tecnología'
);