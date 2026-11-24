CREATE DATABASE entregable_sql; 

-- PRÁCTICA 1 

CREATE TABLE departamentos (
    id_dep     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     TEXT NOT NULL
);


CREATE TABLE empleados (
    id_emp         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    email      VARCHAR(100) NOT NULL,
    salario    NUMERIC NOT NULL,  
    departamento_id    INTEGER REFERENCES departamentos(id_dep)
);

CREATE TABLE proyectos (
    id_proyect        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,  
    fecha_inicio DATE, 
    departamento_id    INTEGER REFERENCES departamentos(id_dep)
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

SELECT * FROM departamentos;
SELECT * FROM empleados;
SELECT * FROM proyectos;

SELECT empleados.nombre
FROM empleados
LEFT JOIN departamentos
ON departamentos.id_dep = empleados.departamento_id
WHERE empleados.departamento_id IS NULL;

SELECT empleados.nombre, empleados.departamento_id
FROM empleados
INNER JOIN departamentos
ON departamentos.id_dep = empleados.departamento_id;

-- Sara no sale 


-- PRÁCTICA 2 

SELECT nombre, salario
FROM empleados
WHERE salario < (
    SELECT AVG(salario) FROM empleados
    );

SELECT nombre, salario
FROM empleados
WHERE salario = (
    SELECT MAX(salario) FROM empleados
    );

SELECT nombre
FROM empleados
WHERE departamento_id IN (
    SELECT id_dep FROM departamentos WHERE nombre='Tecnología'  
);