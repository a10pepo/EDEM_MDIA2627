-----------------
--- Practica 1 --    
-----------------

CREATE TABLE IF NOT EXISTS departamentos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);
CREATE TABLE IF NOT EXISTS empleados(
   id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   nombre VARCHAR (30) NOT NULL,
   email VARCHAR(30) NOT NULL,
   salario INTEGER NOT NULL,
   departamento_id INTEGER REFERENCES departamentos(id)
);
CREATE TABLE IF NOT EXISTS proyectos(
   id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    fecha_inicio DATE,
    departamento_id INTEGER REFERENCES departamentos(id)
);
INSERT INTO departamentos (nombre) VALUES
    ('VentAS'), ('Tecnología'), ('Legal'), ('I+D');
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

SELECT e.nombre, e.departamento_id FROM empleados e
WHERE e.nombre = 'Sara';

SELECT e.nombre, d.nombre AS departamento FROM empleados e
inner JOIN departamentos d 
ON e.departamento_id = d.id;

---------
- EXTRA -
---------
SELECT e.nombre, d.nombre FROM empleados e
RIGHT JOIN departamentos d 
ON e.departamento_id = d.id

-----------------
--- Practica 2 --   
-----------------

SELECT * FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

SELECT * FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

SELECT * FROM empleados 
WHERE departamento_id = (SELECT id FROM departamentos WHERE nombre = 'Tecnología');