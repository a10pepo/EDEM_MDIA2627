CREATE TABLE departamentos(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL
);

CREATE TABLE empleados(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL,
    email VARCHAR(25) NOT NULL,
    salario INTEGER NOT NULL,
    departamento_id INTEGER REFERENCES departamentos(id)
);

CREATE TABLE proyectos(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL,
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

SELECT e.nombre 
FROM empleados AS e
INNER JOIN departamentos AS d
ON d.id = e.departamento_id;


--Practica 2
SELECT nombre, salario 
FROM empleados 
WHERE salario < (SELECT AVG(salario) FROM empleados);
SELECT nombre, salario 
FROM empleados 
WHERE salario = (SELECT MAX(salario) FROM empleados);

SELECT nombre 
FROM empleados 
WHERE departamento_id = (SELECT id FROM departamentos WHERE nombre = 'Tecnología');