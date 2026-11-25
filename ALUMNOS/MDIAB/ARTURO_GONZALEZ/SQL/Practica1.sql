--Practica 1 - SQL

--Crear las tablas y relaciones entre ellas
CREATE TABLE departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL
);
CREATE TABLE empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    id_departamento INTEGER REFERENCES departamentos(id)
);
CREATE TABLE proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    id_departamento INTEGER REFERENCES departamentos(id)
);
--Insertar datos de ejemplo en las tablas
INSERT INTO departamentos (nombre_departamento) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

INSERT INTO empleados
    (nombre, email, salario, id_departamento)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

INSERT INTO proyectos
    (nombre, fecha_inicio, id_departamento)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);


-- Consultar que el depatamento de Sara es NULL
SELECT id_departamento FROM empleados WHERE nombre = 'Sara';

-- Join de todos los empleados con sus departamentos
SELECT * FROM empleados 
INNER JOIN departamentos ON empleados.id_departamento = departamentos.id;
