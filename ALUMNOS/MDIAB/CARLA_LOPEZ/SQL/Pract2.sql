
-- 1. Los empleados que cobran menos que la media
SELECT nombre, salario
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

-- 2. El empleado que más cobra, con MAX en la subconsulta
SELECT nombre, salario
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

-- 3. Los empleados de Tecnología, buscando su id con una subconsulta por nombre
SELECT nombre
FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos
    WHERE nombre = 'Tecnología'
);