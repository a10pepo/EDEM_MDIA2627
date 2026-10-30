---PRÁCTICA 1:---

-- Departamentos
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');
-- Empleados (Sara no tiene departamento)
INSERT INTO empleados
    (nombre, email, salario, departamentos_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);
-- Proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamentos_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos
SELECT * FROM departamentos;
SELECT * FROM empleados;





CREATE TABLE IF NOT EXISTS departamentos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL
);
SELECT * FROM departamentos

CREATE TABLE IF NOT EXISTS empleados (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    salario INTEGER NOT NULL,
    departamentos_id INTEGER REFERENCES departamentos(id)
);
SELECT * FROM empleados

CREATE TABLE IF NOT EXISTS proyectos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    fecha_inicio VARCHAR(40) NOT NULL,
    departamento_id INTEGER REFERENCES departamentos(id)
);
SELECT * FROM proyectos

SELECT * FROM empleados
WHERE nombre='Sara'AND departamentos_id IS NULL;

SELECT * FROM empleados
INNER JOIN departamentos
ON empleados.departamentos_id = departamentos.id 



---PRÁCTICA 2:---
SELECT nombre, salario 
FROM empleados
WHERE salario < (SELECT AVG (salario) FROM empleados);

SELECT nombre, salario 
FROM empleados
WHERE salario = (SELECT MAX (salario) FROM empleados);

SELECT nombre
FROM empleados
WHERE departamentos_id IN (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);