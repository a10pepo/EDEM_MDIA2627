--Crear tabla departamentos
CREATE TABLE departamentos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL
);
-- Departamentos
INSERT INTO departamentos (nombre_departamento) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

-- Ver contenido tabla departamentos
SELECT * FROM departamentos;
-------------------------------------------------------------------------
-- Crear tabla empleados
CREATE TABLE empleados(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    salario FLOAT,
    departamento_id INTEGER REFERENCES departamentos(id)
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

-- Ver contenido tabla empleados
SELECT * FROM empleados;

-------------------------------------------------------------------------
--Crear tabla proyectos
CREATE TABLE proyectos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    departamento_id INTEGER REFERENCES departamentos(id)
);

-- Proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

-- Ver contenido tabla empleados
SELECT * FROM proyectos;
-------------------------------------------------------------------------
--Compruebo que Sara no tiene departamento
SELECT COUNT(*)
FROM empleados JOIN departamentos 
    ON empleados.departamento_id = departamentos.id
WHERE empleados.nombre = 'Sara';

SELECT *
FROM empleados
WHERE nombre = 'Sara';
--Hago un INNER JOIN de cada empleado con su departamento. ¿Quién no sale? --> No sale Sara
SELECT *
FROM empleados INNER JOIN departamentos 
    ON empleados.departamento_id = departamentos.id;
-------------------------------------------------------------------------EXTRA
-- Salen todos los empleados que tengan departamentos
SELECT *
FROM empleados INNER JOIN departamentos 
    ON empleados.departamento_id = departamentos.id;

-- Salen todos los empleados, tengan o no departamentos
SELECT *
FROM empleados LEFT JOIN departamentos 
    ON empleados.departamento_id = departamentos.id;

-- Muestra todos los departamentos, tengan o no empleados asociados
SELECT *
FROM empleados RIGHT JOIN departamentos 
    ON empleados.departamento_id = departamentos.id;

-- Muestra todos los empleados y todos los departamentos, aunque no haya relación entre ellos.
SELECT *
FROM empleados FULL OUTER JOIN departamentos 
    ON empleados.departamento_id = departamentos.id;