CREATE TABLE departamentos (
    id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE empleados (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    salario         NUMERIC(10, 2) NOT NULL,
    departamento_id INTEGER REFERENCES departamentos(id)
);

CREATE TABLE proyectos (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    fecha_inicio    DATE NOT NULL,
    departamento_id INTEGER NOT NULL REFERENCES departamentos(id)
);

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

SELECT * FROM empleados WHERE departamento_id IS NULL;

SELECT * FROM empleados INNER JOIN departamentos ON departamentos.id = empleados.departamento_id;

SELECT nombre, salario FROM empleados
WHERE salario <(SELECT AVG(salario) FROM empleados);

SELECT nombre, salario FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

SELECT nombre FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);
