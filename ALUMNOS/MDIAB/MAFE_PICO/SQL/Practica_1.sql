CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    departamento_id INT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    fecha_inicio DATE NOT NULL,
    departamento_id INT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

-- Inserción de datos
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

-- Comprueba que Sara no tiene departamento.

SELECT *
FROM empleados
LEFT JOIN departamentos ON empleados.departamento_id = departamentos.id
WHERE empleados.nombre = 'Sara';

-- Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale?
SELECT 
    e.nombre AS empleado,
    d.nombre AS departamento
FROM empleados e
INNER JOIN departamentos d 
    ON e.departamento_id = d.id;

-- No sale Sara porque no tiene departamento

-- Une empleados y departamentos con INNER, LEFT y FULL OUTER JOIN, partiendo siempre de empleados.
SELECT *
FROM empleados
INNER JOIN departamentos ON empleados.departamento_id = departamentos.id;

SELECT *
FROM empleados
Left JOIN departamentos ON empleados.departamento_id = departamentos.id;

SELECT *
FROM empleados
FULL OUTER JOIN departamentos ON empleados.departamento_id = departamentos.id;


-- Antes de ejecutar, predice cuántas filas salen y dónde habrá NULL.

-- Encuentra los empleados sin departamento y los departamentos sin empleados con un JOIN e IS NULL.
