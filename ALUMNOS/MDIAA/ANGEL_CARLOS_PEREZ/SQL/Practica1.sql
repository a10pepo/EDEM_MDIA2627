CREATE TABLE departamentos (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     TEXT NOT NULL
);

CREATE TABLE empleados (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    departamento_id    INTEGER REFERENCES departamentos(id),
    nombre      TEXT NOT NULL,
    email       VARCHAR,
    salario     INTEGER
);


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

CREATE TABLE proyectos (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    departamento_id    INTEGER REFERENCES departamentos(id),
    nombre      TEXT NOT NULL,
    fecha_inicio       DATE
);

INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

SELECT * FROM departamentos
SELECT * FROM empleados 
SELECT * FROM proyectos

SELECT * FROM empleados WHERE departamento_id IS NULL;


SELECT
    empleados.nombre,
    departamentos.nombre
FROM empleados
INNER JOIN departamentos ON departamentos.id = empleados.departamento_id;




