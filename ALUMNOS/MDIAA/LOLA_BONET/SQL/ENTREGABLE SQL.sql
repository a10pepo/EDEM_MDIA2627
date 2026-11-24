-----EJERCICIOS SQL3----
---- PRÁCTICA 1 ----
--- 1. Crea la tabla departamentos: es la del «uno», va primero.
CREATE TABLE departamentos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(30)
);

--- 2. Crea empleados y proyectos, cada una con su foreign key departamento_id.
CREATE TABLE empleados(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,
    salario NUMERIC(10,2),
    departamento_id INTEGER REFERENCES departamentos(id)
);

CREATE TABLE proyectos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(70) NOT NULL,
    fecha_inicio TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    departamento_id INTEGER REFERENCES departamentos(id)
);

--- 3. Inserta los datos de la diapositiva anterior.
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

INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

--- 4. Comprueba que Sara no tiene departamento.
SELECT nombre
FROM empleados
WHERE departamento_id is NULL;

--- 5. Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale? Sara
SELECT *
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id;



---- PRÁCTICA 2 ----
--- 1. Los empleados que cobran menos que la media.
SELECT nombre, salario 
FROM empleados
WHERE salario < (SELECT AVG(salario)
                    FROM empleados);

--- 2. El empleado que más cobra, con MAX en la subconsulta.
SELECT nombre, salario 
FROM empleados
WHERE salario = (SELECT MAX(salario)
                    FROM empleados);

--- 3. Los empleados de Tecnología, buscando su id con una subconsulta por nombre.
SELECT nombre
FROM empleados
WHERE empleados.departamento_id = (SELECT id
                                    FROM departamentos
                                    WHERE nombre ='Tecnología');