--Práctica 1

CREATE TABLE departamentos (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre VARCHAR(20)
);

INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

CREATE TABLE empleados (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre VARCHAR(20),
	email VARCHAR(50),
	salario INTEGER NOT NULL,
	departamento_id INTEGER REFERENCES departamentos(id)
);

INSERT INTO empleados (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

CREATE TABLE proyectos (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre VARCHAR(50),
	fecha_inicio VARCHAR(20),
	departamento_id INTEGER REFERENCES departamentos(id)
);

INSERT INTO proyectos (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

SELECT empleados.nombre
FROM empleados
INNER JOIN departamentos
ON departamentos.id = empleados.departamento_id
WHERE empleados.nombre = 'Sara';

SELECT empleados.nombre
FROM empleados
INNER JOIN departamentos
ON departamentos.id = empleados.departamento_id;

SELECT empleados.nombre, departamentos.nombre
FROM empleados
FULL OUTER JOIN departamentos
ON departamentos.id = empleados.departamento_id
WHERE empleados.departamento_id IS NULL;

--Práctica 2

SELECT empleados.nombre, empleados.salario
FROM empleados
WHERE empleados.salario < (SELECT AVG(empleados.salario) FROM empleados);

SELECT empleados.nombre, empleados.salario
FROM empleados
WHERE empleados.salario = (SELECT MAX(empleados.salario) FROM empleados);

SELECT empleados.nombre
FROM empleados
WHERE departamento_id IN (SELECT departamentos.id FROM departamentos WHERE departamentos.nombre = 'Tecnología');
