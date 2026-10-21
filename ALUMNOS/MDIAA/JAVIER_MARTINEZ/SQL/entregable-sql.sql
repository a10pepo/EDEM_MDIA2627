-- CREAMOS TABLAS E INSERTAMOS
CREATE TABLE  departamentos (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(50)
);
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

CREATE TABLE  empleados (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(50),
    email      VARCHAR(50),
    salario    INTEGER,
    departamento_id  INTEGER REFERENCES departamentos(id)
);
DROP TABLE empleados;
INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

CREATE TABLE proyectos (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(50),
    fecha_inicio     VARCHAR(50),
    departamento_id  INTEGER REFERENCES departamentos(id)
)

INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);


-- Comprueba que Sara no tiene departamento.
-- Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale?

SELECT nombre, departamento_id AS departamento
FROM empleados
WHERE nombre ='Sara';

SELECT empleados.nombre, departamentos.nombre
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id;

-- EXTRAS
SELECT empleados.nombre, departamentos.nombre
FROM empleados
LEFT JOIN departamentos
ON empleados.departamento_id = departamentos.id;

SELECT empleados.nombre, departamentos.nombre
FROM empleados
RIGHT JOIN departamentos
ON empleados.departamento_id = departamentos.id;

SELECT empleados.nombre, departamentos.nombre
FROM empleados
FULL OUTER JOIN departamentos
ON empleados.departamento_id = departamentos.id;


SELECT 
    empleados.nombre AS empleado, 
    departamentos.nombre AS departamento
FROM empleados
FULL OUTER JOIN departamentos 
    ON empleados.departamento_id = departamentos.id
WHERE empleados.departamento_id IS NULL 
   OR departamentos.id IS NULL;

-- PRACTICA-2

SELECT empleados.nombre
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

-- Empleado que mas cobra con MAX en la subconsulta

SELECT empleados.nombre
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

-- Los empleados de Tecnología, buscando su id con una subconsulta por nombre.
 SELECT empleados.nombre
 FROM empleados
 WHERE departamento_id = (SELECT id FROM departamentos WHERE nombre='Tecnología');