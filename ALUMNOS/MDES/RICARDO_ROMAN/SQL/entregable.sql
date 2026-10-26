CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    salario DECIMAL(10, 2) NOT NULL,
    departamento_id INT REFERENCES departamentos(id)
);

CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    departamento_id INT REFERENCES departamentos(id)
);

-- Departamentos
INSERT INTO departamentos (nombre) VALUES
('Ventas'), ('Tecnología'), ('Legal'), ('I+D');


-- Empleados (Sara no tiene departamento)
INSERT INTO empleados
(nombre, email, salario, departamento_id)
VALUES
('Ana', 'ana@empresa.com', 52000, 2),
('Luis', 'luis@empresa.com', 38000, 2),
('Marta', 'marta@empresa.com', 45000, 1),
('Pablo', 'pablo@empresa.com', 31000, 1),
('Sara', 'sara@empresa.com', 29000, NULL)


-- Proyectos
INSERT INTO proyectos
(nombre, fecha_inicio, departamento_id)
VALUES
('Web nueva', '2026-09-01', 2),
('App móvil', '2026-11-15', 2),
('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

-- PRACTICA 1
-- Comprobar que Sara no tiene departamento
SELECT *
FROM empleados
WHERE nombre = 'Sara'
AND departamento_id IS NULL;

-- Empleados + dptos
SELECT *
FROM empleados AS e
INNER JOIN departamentos AS d
ON e.departamento_id = d.id
-- NO sale Sara ya que no tiene departamento y se queda fuera del inner join

-- Extra

-- INNER ( sin Nulls)
SELECT *
FROM empleados AS e
INNER JOIN departamentos AS d
ON e.departamento_id = d.id

-- LEFT (Null en empleados sin departamentos)
SELECT *
FROM empleados AS e
LEFT JOIN departamentos AS d
ON e.departamento_id = d.id

-- RIGHT (Null en los departamentos sin empleados)
SELECT *
FROM empleados AS e
RIGHT JOIN departamentos AS d
ON e.departamento_id = d.id2

-- Outer (Null en los departamentos sin empleados y empleados sin departamento)
SELECT *
FROM empleados AS e
FULL OUTER JOIN departamentos AS d
ON e.departamento_id = d.id

-- Sacar las personas con su departamento (si existe)
SELECT e.nombre AS nombre_empl, d.nombre AS nombre_dpto
FROM empleados AS e
LEFT JOIN departamentos AS d
ON e.departamento_id = d.id

SELECT * FROM departamentos


-- PRACTICA 2

-- Cobran menos que la media
SELECT e.nombre , e.salario
FROM empleados AS e
WHERE e.salario < (
    SELECT AVG(salario) FROM empleados 
)

-- El que mas cobra
SELECT e.nombre , e.salario
FROM empleados AS e
WHERE e.salario = (
    SELECT MAX(salario) FROM empleados 
)

-- Empleados de Tecnologia por su id con subconsulta por nombre
SELECT nombre
FROM empleados
WHERE departamento_id IN (
    SELECT id
    FROM departamentos
    WHERE nombre = 'Tecnología'

)


