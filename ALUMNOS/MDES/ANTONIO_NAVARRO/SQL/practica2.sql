-- Los que cobran menos que la media
SELECT nombre, salario
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

-- El que más cobra
SELECT nombre, salario
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

-- Los empleados de Tecnología
SELECT nombre
FROM empleados
WHERE departamento_id = (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);