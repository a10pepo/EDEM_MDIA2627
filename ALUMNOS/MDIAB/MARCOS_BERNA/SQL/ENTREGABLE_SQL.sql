-- Práctica 1

DROP TABLE IF EXISTS proyectos;
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS departamentos;

-- Crear tabla departamentos

CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Crear tabla empleados

CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    salario DECIMAL(10,2),
    departamento_id INT,

    FOREIGN KEY (departamento_id)
    REFERENCES departamentos(id)
);

-- Crear tabla proyectos

CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    departamento_id INT,

    FOREIGN KEY (departamento_id)
    REFERENCES departamentos(id)
);

-- Insertar departamentos

INSERT INTO departamentos (nombre)
VALUES
('Ventas'),
('Tecnología'),
('Legal'),
('I+D');

-- Insertar empleados

INSERT INTO empleados
(nombre, email, salario, departamento_id)
VALUES
('Ana', 'ana@empresa.com', 52000, 2),
('Luis', 'luis@empresa.com', 38000, 2),
('Marta', 'marta@empresa.com', 45000, 1),
('Pablo', 'pablo@empresa.com', 31000, 1),
('Sara', 'sara@empresa.com', 29000, NULL);

-- Insertar proyectos

INSERT INTO proyectos
(nombre, fecha_inicio, departamento_id)
VALUES
('Web nueva', '2026-09-01', 2),
('App móvil', '2026-11-15', 2),
('Campaña de verano', '2027-05-01', 1);

-- Ver empleados sin departamento

SELECT *
FROM empleados
WHERE departamento_id IS NULL;

-- Relacionar empleados y departamentos

SELECT
    e.nombre AS empleado,
    d.nombre AS departamento
FROM empleados e
INNER JOIN departamentos d
ON e.departamento_id = d.id;

-- Práctica 2 - Subconsultas

-- Empleados que cobran menos que la media

SELECT *
FROM empleados
WHERE salario < (
    SELECT AVG(salario)
    FROM empleados
);

-- Empleado que más cobra

SELECT *
FROM empleados
WHERE salario = (
    SELECT MAX(salario)
    FROM empleados
);

-- Empleados del departamento Tecnología

SELECT *
FROM empleados
WHERE departamento_id = (
    SELECT id
    FROM departamentos
    WHERE nombre = 'Tecnología'
);