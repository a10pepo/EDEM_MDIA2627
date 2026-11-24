CREATE DATABASE entregable_sql;

CREATE TABLE departamentos (
    departamento_id INTEGER PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE empleados (
    id_empleados INTEGER    PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(150),
    salario NUMERIC(10,2),
    departamento_id INTEGER REFERENCES departamentos(departamento_id)
);

CREATE TABLE proyectos (
    id_proyectos INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    fecha_inicio DATE,
    departamento_id INTEGER REFERENCES departamentos(departamento_id)
);

INSERT INTO departamentos (departamento_id, nombre) VALUES
    ('1', 'Ventas'), ('2', 'Tecnología'), ('3', 'Legal'), ('4', 'I+D');

INSERT INTO empleados
    (id_empleados, nombre, email, salario, departamento_id)
VALUES
    ('1', 'Ana',   'ana@empresa.com',   52000, 2),
    ('2', 'Luis',  'luis@empresa.com',  38000, 2),
    ('3', 'Marta', 'marta@empresa.com', 45000, 1),
    ('4','Pablo', 'pablo@empresa.com', 31000, 1),
    ('5','Sara',  'sara@empresa.com',  29000, NULL);

INSERT INTO proyectos
    (id_proyectos, nombre, fecha_inicio, departamento_id)
VALUES
    ('1', 'Web nueva',         '2026-09-01', 2),
    ('2', 'App móvil',         '2026-11-15', 2),
    ('3', 'Campaña de verano', '2027-05-01', 1);

SELECT *
FROM empleados
WHERE nombre = 'Sara';

SELECT *
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.departamento_id;

SELECT *
FROM empleados
LEFT JOIN departamentos
ON empleados.departamento_id = departamentos.departamento_id;

SELECT *
FROM empleados
FULL OUTER JOIN departamentos
ON empleados.departamento_id = departamentos.departamento_id;

SELECT *
FROM empleados
LEFT JOIN departamentos
ON empleados.departamento_id = departamentos.departamento_id
WHERE departamentos.departamento_id IS NULL;

SELECT *
FROM empleados
RIGHT JOIN departamentos
ON empleados.departamento_id = departamentos.departamento_id
WHERE empleados.id_empleados IS NULL;