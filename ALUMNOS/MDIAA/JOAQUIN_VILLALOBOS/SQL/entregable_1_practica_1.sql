-- Crear Tabla Departamentos
CREATE TABLE departamentos (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(50)
);

-- Añadir Valores en Departamentos
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

-- Crear Tabla Empleados
CREATE TABLE empleados (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(50),
    email     VARCHAR(100),
    salario     INTEGER,
    departamento_id    INTEGER REFERENCES departamentos(id)
);

-- Empleados (Sara no tiene departamento)
INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

-- Crear Tabla Proyectos
CREATE TABLE proyectos (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(50),
    fecha_inicio     VARCHAR(100),
    departamento_id    INTEGER REFERENCES departamentos(id)
);

-- Proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

-- Comprueba que Sara no tiene departamento
SELECT *
FROM empleados
WHERE departamento_id IS NULL;

SELECT empleados.nombre
FROM empleados
WHERE departamento_id IS NULL;

-- INNER JOIN de cada empleado con su departamento
SELECT empleados.nombre, departamentos.nombre
FROM departamentos
INNER JOIN empleados
ON departamentos.id = empleados.departamento_id;

SELECT *
FROM departamentos
INNER JOIN empleados
ON departamentos.id = empleados.departamento_id;