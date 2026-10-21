CREATE TABLE departamentos (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(20) NOT NULL
);

INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

CREATE TABLE empleados (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    departamento_id      INTEGER REFERENCES departamentos(id),
    nombre        VARCHAR(100) NOT NULL,
    email         VARCHAR(200),
    salario       INT
);

INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

CREATE TABLE proyectos (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    departamento_id      INTEGER REFERENCES departamentos(id),
    nombre        VARCHAR(100) NOT NULL,
    fecha_inicio    DATE
);

INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

SELECT * FROM empleados WHERE departamento_id IS NULL

SELECT empleados.nombre, departamentos.nombre
FROM empleados
INNER JOIN departamentos ON departamentos.id = empleados.departamento_id 

SELECT * 
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados)

SELECT * 
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados)

SELECT * 
FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);