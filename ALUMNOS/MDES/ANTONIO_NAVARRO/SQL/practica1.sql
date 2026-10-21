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



-- Sara no tiene departamento
SELECT nombre FROM empleados WHERE departamento_id IS NULL;

-- Cada empleado con su departamento
SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM empleados
INNER JOIN departamentos ON departamentos.id = empleados.departamento_id;


-- Inserciones de la presentación

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


