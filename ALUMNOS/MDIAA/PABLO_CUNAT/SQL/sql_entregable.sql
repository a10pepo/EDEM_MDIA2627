----- PRACTICA 1 ---------------------------------------------------------------------------------------------

CREATE TABLE users (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(255) UNIQUE NOT NULL
);
INSERT INTO users (first_name, last_name, email) VALUES
    ('Ada', 'Lovelace', 'ada@example.com'),
    ('Luffy', 'Monkey D.', 'luffy@mugiwara.com'),
    ('Zoro', 'Roronoa', 'zoro@mugiwara.com'),
    ('Sanji', 'Vinsmoke', 'sanji@mugiwara.com');

CREATE TABLE posts (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    title        VARCHAR(100) NOT NULL,
    body         TEXT,
    publish_date TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
INSERT INTO posts (user_id, title, body) VALUES
    (1, 'Post One', 'This is post one'),
    (3, 'Post Two', 'This is post two'),
    (1, 'Post Three', 'This is post three'),
    (2, 'Post Four', 'This is post four'),
    (1, 'Post Five', 'This is post five'),
    (2, 'Post Six', 'This is post six'),
    (1, 'Post Seven', 'This is post seven'),
    (3, 'Post Eight', 'This is post eight');
CREATE TABLE comments (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    post_id    INTEGER NOT NULL REFERENCES posts(id),
    user_id    INTEGER NOT NULL REFERENCES users(id),
    body       TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
INSERT INTO comments (post_id, user_id, body) VALUES
    (1, 3, 'This is comment one'),
    (2, 1, 'This is comment two'),
    (5, 3, 'This is comment three'),
    (2, 2, 'This is comment four'),
    (1, 2, 'This is comment five');


---Crea la tabla departamentos: es la del «uno», va primero.
CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Crea empleados y proyectos, cada una con su foreign key departamento_id.

CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    salario NUMERIC(10,2),
    departamento_id INTEGER REFERENCES departamentos(id)
);

-- Creamos PROYECTOS
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    departamento_id INTEGER NOT NULL REFERENCES departamentos(id)
);

-- Inserta los datos de la diapositiva anterior.

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

------------------------------------------------------- CONSULTAS ---------------------------------------------
--Comprueba que Sara no tiene departamento.

SELECT * FROM empleados
WHERE nombre='Sara'AND departamento_id IS NULL;

---- Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale?

SELECT * FROM empleados
INNER JOIN departamentos ON empleados.departamento_id=departamentos.id;

---------------------- PRACTICA 2 ------------------------------------------------------------------------

--Los empleados que cobran menos que la media.

SELECT * FROM empleados
WHERE salario<(
    SELECT AVG(salario) FROM empleados);

SELECT AVG(salario) FROM empleados;

------ El empleado que más cobra, con MAX en la subconsulta.

SELECT * FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

---- Los empleados de Tecnología, buscando su id con una subconsulta por nombre.

SELECT * FROM empleados
WHERE departamento_id in (SELECT id FROM departamentos WHERE nombre ='Tecnología');



