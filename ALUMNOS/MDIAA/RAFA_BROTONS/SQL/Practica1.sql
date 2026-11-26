CREATE TABLE departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE empleados (
     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
     nombre VARCHAR(100) NOT NULL,
     email VARCHAR(100) NOT NULL,
     salario NUMERIC (10,2),
     departamento_id INTEGER  REFERENCES departamentos(id)
);

CREATE TABLE proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR,
    fecha_inicio DATE,
    departamento_id INTEGER NOT NULL REFERENCES departamentos(id)
);
    

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


--comprobacion de que sara sale como null en el departamento
SELECT nombre, departamento_id
FROM empleados
WHERE nombre = 'Sara';

--comprobacion de que cada empleado sale con el nombre de su departamento (sara no sale ya que no tiene departamento)
SELECT empleados.nombre, departamentos.nombre
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id;