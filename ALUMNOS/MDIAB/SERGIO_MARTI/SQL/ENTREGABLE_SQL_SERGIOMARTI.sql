--Practica1
CREATE TABLE departamento (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50)
    );

CREATE TABLE empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50), 
    email VARCHAR(100),
    salario NUMERIC(10,2),
    departamento_id INTEGER REFERENCES departamento(id)
    );

CREATE TABLE proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50),
    fecha_inicio DATE,
    departamento_id INTEGER REFERENCES departamento(id)
    );

-- Departamentos
INSERT INTO departamento (nombre) VALUES
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

SELECT nombre FROM empleados WHERE departamento_id IS NULL;

SELECT * FROM departamento 
INNER JOIN empleados ON departamento.id = empleados.departamento_id

--Practica2

SELECT nombre, salario FROM empleados WHERE salario < (SELECT AVG(salario) FROM empleados);

SELECT nombre, salario FROM empleados WHERE salario = (SELECT MAX(salario) FROM empleados);

SELECT nombrE 
FROM empleados 
WHERE departamento_id = (
    SELECT id
    FROM departamento
    WHERE nombre = 'Tecnología'
);