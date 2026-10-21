CREATE TABLE IF NOT EXISTS departamentos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS empleados (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    salario INTEGER NOT NULL,
    departamento_id BIGINT REFERENCES departamentos(id)
);

CREATE TABLE IF NOT EXISTS proyectos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    fecha_inicio TIMESTAMPTZ NOT NULL,
    departamento_id BIGINT REFERENCES departamentos(id)
);


--Departamentos
INSERT INTO departamentos (nombre) VALUES
('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

--Empleados (Sara no tiene departamento)
INSERT INTO empleados
(nombre, email, salario, departamento_id)
VALUES
('Ana',   'ana@empresa.com',   52000, 2),
('Luis',  'luis@empresa.com',  38000, 2),
('Marta', 'marta@empresa.com', 45000, 1),
('Pablo', 'pablo@empresa.com', 31000, 1),
('Sara',  'sara@empresa.com',  29000, NULL);

--Proyectos
INSERT INTO proyectos
(nombre, fecha_inicio, departamento_id)
VALUES
('Web nueva',         '2026-09-01', 2),
('App móvil',         '2026-11-15', 2),
('Campaña de verano', '2027-05-01', 1);

--Legal e I+D no tienen empleados--ni proyectos

-- Comprueba que Sara no tiene departamento.
SELECT nombre, departamento_id
FROM empleados
WHERE nombre = 'Sara' AND departamento_id IS NULL;
-- Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale?
SELECT *
FROM empleados 
INNER JOIN departamentos 
ON empleados.departamento_id = departamentos.id;



-- 1. Los empleados que cobran menos que la media.
SELECT * 
FROM empleados
WHERE salario < (
    SELECT AVG(salario)
    FROM empleados
);
-- 2. El empleado que más cobra, con MAX en la subconsulta.
SELECT * 
FROM empleados
WHERE salario = (
    SELECT MAX(salario)
    FROM empleados
);
-- 3. Los empleados de Tecnología, buscando su id con una subconsulta por nombre.
SELECT *
FROM empleados
WHERE departamento_id IN(
    SELECT id
    FROM departamentos
    WHERE nombre = 'Tecnología'
);