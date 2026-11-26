CREATE TABLE departamentos (
    id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE empleados (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    salario         NUMERIC(10, 2) NOT NULL,
    departamento_id INTEGER REFERENCES departamentos(id)   -- sin NOT NULL, por Sara
);

CREATE TABLE proyectos (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    fecha_inicio    DATE NOT NULL,
    departamento_id INTEGER NOT NULL REFERENCES departamentos(id)
);


INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');
-- Quedan así: Ventas=1, Tecnología=2, Legal=3, I+D=4


INSERT INTO empleados (nombre, email, salario, departamento_id) VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

INSERT INTO proyectos (nombre, fecha_inicio, departamento_id) VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

-- Comprueba que Sara no tiene departamento
SELECT nombre 
FROM empleados 
WHERE nombre = 'Sara' AND departamento_id IS NULL;

-- Haz un INNER JOIN de cada empleado con su departamento. Quien no sale? Sara

SELECT * FROM empleados
INNER JOIN departamentos ON departamentos.id = empleados.departamento_id;

--- Practica 2 ---

-- Los que cobran menos que la media

SELECT nombre, salario
FROM empleados
WHERE salario < (
    SELECT AVG(salario) FROM empleados);

-- El empleado que mas cobra

SELECT nombre, salario
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

-- Los empleados de Tecnología, buscando su id con una subconsulta por nombre.

SELECT nombre
FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);