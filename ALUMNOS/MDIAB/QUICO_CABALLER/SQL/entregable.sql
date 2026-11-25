-- --Crear tabla departamento
create table departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre varchar(50) not null
);
-- --Crea empleados y proyectos, cada una con su foreign key departamento_id.
create table empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre varchar(50) not null,
    email varchar(100) not null unique,
    salario numeric(10, 2) not null,
    departamento_id int references departamentos(id)
);
create table proyectos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre varchar(100) not null,
    fecha_inicio date not null,
    departamento_id int references departamentos(id)
);

-- -- Departamentos
INSERT INTO departamentos (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

-- -- Empleados (Sara no tiene departamento)
INSERT INTO empleados
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);

-- -- Proyectos
INSERT INTO proyectos
    (nombre, fecha_inicio, departamento_id)
VALUES
    ('Web nueva',         '2026-09-01', 2),
    ('App móvil',         '2026-11-15', 2),
    ('Campaña de verano', '2027-05-01', 1);

-- -- Legal e I+D no tienen empleados

-- ni proyectos
SELECT * 
from empleados e
where e.nombre = 'Sara';
        --departamento_id es null, por lo que no tiene departamento asignado.

--Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale?
select e.nombre, d.nombre as departamento
from empleados e
inner join departamentos d on e.departamento_id = d.id;
        ---Sara no sale porque no tiene departamento asignado, por lo que su departamento_id es null y no hay coincidencia en el INNER JOIN.

--Los empleados que cobran menos que la media.
select e.nombre, e.salario
from empleados e
where e.salario < (select avg(salario) from empleados);

--El empleado que más cobra, con MAX en la subconsulta.
select e.nombre, e.salario
from empleados e
where e.salario = (select max(salario) from empleados);

--Los empleados de Tecnología, buscando su id con una subconsulta por nombre.
select e.nombre, e.salario
from empleados e
where e.departamento_id = (select id from departamentos where nombre = 'Tecnología');