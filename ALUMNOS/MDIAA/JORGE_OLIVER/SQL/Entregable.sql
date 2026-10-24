--Práctica 1:
--CREAR TABLA DEPARTAMENTOS

CREATE TABLE departamento (

);

ALTER TABLE departamento
ADD id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
ADD nombre VARCHAR;


INSERT INTO departamento (nombre) VALUES
('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

--CREAR TABLA EMPLEADOS

CREATE TABLE empleados (
    id BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR,
    email VARCHAR,
    salario INTEGER,
    departamento_id INTEGER REFERENCES departamento(id)
);

SELECT * FROM proyectos;

ALTER TABLE empleados
ADD nombre  VARCHAR;

INSERT INTO empleados
(nombre, email, salario, departamento_id)
VALUES
('Ana', 'ana@empresa.com', 52000, 2),
('Luis', 'luis@empresa.com', 38000, 2),
('Marta', 'marta@empresa.com', 45000, 1),
('Pablo', 'pablo@empresa.com', 31000, 1),
('Sara', 'sara@empresa.com', 29000, NULL);

--CREAR TABLA PROYECTOS

CREATE TABLE proyectos (
    nombre VARCHAR,
    fecha_inicio TIMESTAMPTZ,
    departamento_id INTEGER REFERENCES departamento(id)
);

INSERT INTO proyectos
(nombre, fecha_inicio, departamento_id)
VALUES
('Web nueva', '2026-09-01', 2),
('App móvil', '2026-11-15', 2),
('Campaña de verano', '2027-05-01', 1);

-- Preguntas 1:

SELECT * FROM empleados
WHERE nombre = 'Sara' AND departamento_id IS NULL;

SELECT * FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamento_id;

--PRÁCTICA 2
--1
SELECT nombre, salario
FROM empleados
WHERE salario < (
    SELECT AVG(salario) 
    FROM empleados
);
--2
SELECT nombre, salario
FROM empleados
WHERE salario = (
    SELECT MAX(salario)
    FROM empleados
);
--3
SELECT nombre
FROM empleados
WHERE empleados.departamento_id
IN (
    SELECT departamentos.id
    FROM departamentos
    WHERE departamentos.nombre = 'Tecnología'
);
