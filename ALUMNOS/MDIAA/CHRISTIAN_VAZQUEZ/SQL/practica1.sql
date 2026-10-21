CREATE TABLE departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR (20)
)

CREATE TABLE empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR (20),
    email VARCHAR(50),
    salario INTEGER,
    departamento_id INTEGER REFERENCES departamentos(id)
)

CREATE TABLE proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR (100),
    fecha_inicio VARCHAR(10),
    departamento_id INTEGER REFERENCES departamentos(id)
)

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

-- Comprueba que Sara no tiene departamento
SELECT nombre, departamento_id FROM empleados
WHERE departamento_id IS NULL;

-- INNER JOIN de cada empleado con su departamento
SELECT e.nombre, d.nombre FROM empleados AS e
INNER JOIN departamentos AS d
    ON d.id = e.departamento_id;