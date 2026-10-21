CREATE TABLE IF NOT EXISTS departamentos(
    id     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS empleados(
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(100),
    email           VARCHAR(100),
    salario         NUMERIC(10,3),
    departamento_id INTEGER REFERENCES departamentos(id)
);

CREATE TABLE IF NOT EXISTS proyectos(
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(100),
    fecha_inicio    VARCHAR(100),
    departamento_id INTEGER REFERENCES departamentos(id)
);

INSERT INTO departamentos (nombre) VALUES
('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

INSERT INTO empleados
(nombre, email, salario, departamento_id)
VALUES
('Ana', 'ana@empresa.com', 52000, 2),
('Luis', 'luis@empresa.com', 38000, 2),
('Marta', 'marta@empresa.com', 45000, 1),
('Pablo', 'pablo@empresa.com', 31000, 1),
('Sara', 'sara@empresa.com', 29000, NULL);
-- Empleados (Sara no tiene departamento)

INSERT INTO proyectos
(nombre, fecha_inicio, departamento_id)
VALUES
('Web nueva', '2026-09-01', 2),
('App móvil', '2026-11-15', 2),
('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados ni proyectos

SELECT * FROM empleados WHERE nombre = 'Sara';

SELECT * FROM empleados AS e INNER JOIN departamentos AS d ON e.departamento_id = d.id;
--- SARA NO SALE PORQUE NO TIENE DEPARTAMENTO

SELECT nombre, salario 
FROM empleados
WHERE salario <= (SELECT AVG(salario) FROM empleados);

SELECT nombre
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

SELECT e.nombre, d.nombre 
FROM empleados AS e INNER JOIN departamentos AS d
ON d.id = e.departamento_id
WHERE d.nombre = (SELECT nombre FROM departamentos WHERE nombre = 'Tecnología')