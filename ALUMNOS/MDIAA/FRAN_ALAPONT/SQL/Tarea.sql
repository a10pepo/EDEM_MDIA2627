-- Aquí tengo el código previo a la tarea
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

-- Todos los posts, con su usuario
SELECT *
FROM users
INNER JOIN posts
ON users.id = posts.user_id;

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

-- Todos los usuarios, tengan posts o no
SELECT users.first_name, posts.title
FROM users
LEFT JOIN posts
ON users.id = posts.user_id;

-- Usuarios sin ninguna publicación
SELECT users.first_name
FROM users
LEFT JOIN posts
ON users.id = posts.user_id
WHERE posts.id IS NULL;

SELECT
    comments.body,
    posts.title,
    users.first_name,
    users.last_name
FROM comments
INNER JOIN posts ON posts.id = comments.post_id
INNER JOIN users ON users.id = comments.user_id;



























-- Comienzo de la tarea:
-- Departamentos
CREATE TABLE departamentos(
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre     TEXT NOT NULL
);
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');
-- Empleados (Sara no tiene departamento)
CREATE TABLE empleados(
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          TEXT NOT NULL,
    email           TEXT NOT NULL,
    salario         INTEGER,
    departamento_id INTEGER REFERENCES departamentos(id)
);
INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

CREATE TABLE proyectos(
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          TEXT NOT NULL,
    fecha_inicio    DATE,
    departamento_id INTEGER REFERENCES departamentos(id)
);

-- Proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados
-- ni proyectos

SELECT * FROM empleados
WHERE nombre= 'Sara' AND departamentos_id IS NULL;

SELECT * FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id;

SELECT * FROM empleados
WHERE salario < (
    SELECT AVG(salario) FROM empleados    
);

SELECT * FROM empleados
WHERE salario = (
    SELECT MAX(salario) FROM empleados    
);

SELECT * FROM empleados
WHERE departamento_id in (
    SELECT id FROM departamentos WHERE nombre='Tecnología'    
);