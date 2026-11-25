-- PRACTICA 1
-- Crear las tablas 
CREATE TABLE departamentos (
    id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  VARCHAR(30)
) ;

CREATE TABLE empleados (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(30),
    email           VARCHAR(100),
    salario         INTEGER,
    departamento_id BIGINT REFERENCES departamentos(id)
) ;

CREATE TABLE proyectos (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(30),
    fecha_inicio    VARCHAR(10),
    departamento_id BIGINT NOT NULL REFERENCES departamentos(id)
) ; 

-- Insertar datos en las tablas 
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

-- Comprobar que Sara no tiene departamento
SELECT nombre, departamento_id
FROM empleados
WHERE departamento_id IS NULL ;

-- INNER JOIN de cada empleado con su departamento
SELECT empleados.nombre, departamentos.nombre
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id ;

-- PRACTICA 2
-- Empleados que cobran menos de la media
SELECT nombre
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados) ;

-- El empleado que mas cobra
SELECT nombre
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados) ;

-- Los empleados de Tecnologia
SELECT nombre
FROM empleados
WHERE departamento_id = (SELECT id FROM departamentos WHERE nombre = 'Tecnología') ;