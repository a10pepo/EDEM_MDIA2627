--Practica1

--Crear tablas
CREATE TABLE departamentos (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre       VARCHAR(40) NOT NULL
);

CREATE TABLE empleados (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    departamento_id INTEGER REFERENCES departamentos(id),
    nombre     VARCHAR(40) NOT NULL,
    email VARCHAR(40),
    salario INTEGER    
);

CREATE TABLE proyectos(
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  VARCHAR(40),
    fecha_inicio  VARCHAR(40),
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

--Seleccion
SELECT *
FROM empleados
WHERE nombre='Sara'
AND departamento_id IS NULL;

--Inner Join
SELECT *
FROM empleados
INNER JOIN  departamentos
ON empleados.departamento_id=departamentos.id

--Practica2

-- Los que cobran menos que la media
SELECT nombre, salario
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

--El empleado que mas cobra
SELECT nombre,salario
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

--Los empleados de tech
SELECT nombre
FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);