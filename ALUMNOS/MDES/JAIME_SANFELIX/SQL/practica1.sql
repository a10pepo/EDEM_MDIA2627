CREATE TABLE IF NOT EXISTS departamentos (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS empleados (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(20),
    email      VARCHAR(50),
    salario    INTEGER,
    departamento_id INTEGER REFERENCES departamentos(id)
);


CREATE TABLE IF NOT EXISTS proyectos (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     VARCHAR(20),
    fecha_inicio    VARCHAR(15),
    departamento_id INTEGER NOT NULL REFERENCES departamentos(id)
);

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

-- Proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

SELECT * FROM empleados;

SELECT empleados.nombre, departamentos.nombre FROM empleados INNER JOIN departamentos ON departamentos.id = empleados.departamento_id;