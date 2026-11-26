--Práctica 1:
--1.1
CREATE TABLE departamentos (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR NOT NULL
);

--1.2
CREATE TABLE empleados (
    id                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre              VARCHAR NOT NULL,
    email               VARCHAR,
    salario             INTEGER,
    departamento_id     INTEGER REFERENCES departamentos(id)
);

CREATE TABLE proyectos (
    id                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre              VARCHAR NOT NULL,
    fecha_inicio        DATE,
    departamento_id     INTEGER REFERENCES departamentos(id)
);

--1.3
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

--1.4
SELECT * FROM empleados WHERE nombre = 'Sara';

--1.5
SELECT * FROM empleados INNER JOIN departamentos ON empleados.departamento_id = departamentos.id;


--Práctica 1. Extra:
--1.E.1
SELECT * FROM empleados RIGHT JOIN departamentos ON empleados.departamento_id = departamentos.id;

SELECT * FROM empleados LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id;

SELECT * FROM empleados FULL OUTER JOIN departamentos ON empleados.departamento_id = departamentos.id;

--1.E.3
SELECT empleados.nombre FROM empleados LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id WHERE empleados.departamento_id IS NULL;

SELECT departamentos.nombre FROM empleados RIGHT JOIN departamentos ON empleados.departamento_id = departamentos.id WHERE empleados.nombre IS NULL;


--Práctica 2:

--2.1
SELECT * FROM empleados WHERE empleados.salario <
    (SELECT AVG(salario) FROM empleados);

--2.2
SELECT * FROM empleados WHERE empleados.salario =
    (SELECT MAX(salario) FROM empleados);

--2.3
SELECT * FROM empleados WHERE empleados.departamento_id =
    (SELECT id FROM departamentos WHERE nombre = 'Tecnología');