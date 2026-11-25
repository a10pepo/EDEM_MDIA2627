-- =======================================================
-- PRÁCTICA 2: SUBCONSULTAS
-- =======================================================

-- Ejecuta primero practica1.sql: allí se crean las tablas y se cargan salarios de ejemplo.

-- 1. Los empleados que cobran menos que la media
SELECT 
    id, 
    nombre, 
    salario, 
    departamento_id
FROM empleados
WHERE salario < (
    SELECT AVG(salario) 
    FROM empleados
);

-- 2. El empleado que más cobra, con MAX en la subconsulta
SELECT 
    id, 
    nombre, 
    salario, 
    departamento_id
FROM empleados
WHERE salario = (
    SELECT MAX(salario) 
    FROM empleados
);

-- 3. Los empleados de Tecnología, buscando su id con una subconsulta por nombre
SELECT 
    id, 
    nombre, 
    salario, 
    departamento_id
FROM empleados
WHERE departamento_id = (
    SELECT id 
    FROM departamentos 
    WHERE nombre = 'Tecnología'
);
