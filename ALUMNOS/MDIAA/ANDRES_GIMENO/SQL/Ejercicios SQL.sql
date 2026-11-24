

                                                --PRÁCTICA 1---

--- CREAR LAS TABLAS

CREATE TABLE departamentos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR (100)
);


CREATE TABLE empleados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    salario NUMERIC(7,2),
    departamento_id INTEGER REFERENCES departamentos(id)

);



CREATE TABLE proyectos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR (100),
    fecha_inicio TIMESTAMP,
    departamento_id INTEGER REFERENCES departamentos(id)

);

--- INSERTAR DATOS

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

--- Comprueba que Sara no tiene departamento.

SELECT nombre
FROM empleados
WHERE nombre = 'Sara' and departamento_id IS NULL

--- Haz un INNER JOIN de cada empleado con su departamento. ¿Quién no sale?

SELECT *
FROM empleados
INNER JOIN departamentos
ON empleados.departamento_id = departamentos.id;

                                                    ---EXTRA---

SELECT *
FROM empleados 
LEFT JOIN departamentos
ON empleados.departamento_id = departamentos.id;

##################################################################################################################

SELECT *
FROM empleados
FULL OUTER JOIN departamentos
ON empleados.departamento_id = departamentos.id;

##################################################################################################################

SELECT E.nombre
FROM empleados AS E
LEFT JOIN departamentos AS D
ON E.departamento_id = D.id
WHERE D.id IS NULL;

##################################################################################################################

SELECT D.nombre
FROM departamentos AS D
FULL OUTER JOIN empleados AS E
ON E.departamento_id = D.id
WHERE E.id IS NULL;

##################################################################################################################
##################################################################################################################
##################################################################################################################

                                                --PRÁCTICA 2---
---1. Los empleados que cobran menos

SELECT nombre
FROM empleados 
WHERE salario < (SELECT AVG(salario)
                FROM empleados
);

##################################################################################################################

---2. El empleado que más cobra, con el MAX en la subconsulta

SELECT nombre
FROM empleados 
WHERE salario = (SELECT MAX(salario)
                FROM empleados
);

##################################################################################################################

---3. Los empleados de Tecnología, buscando su id con una subconsulta por nombre.

SELECT nombre
FROM empleados
WHERE departamento_id IN (
    SELECT id 
    FROM departamentos
    WHERE nombre = 'Tecnología'
)