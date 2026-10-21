SELECT nombre, salario
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

SELECT nombre, salario 
FROM empleados 
WHERE salario = (SELECT MAX(salario)FROM empleados)

SELECT nombre
FROM empleados
WHERE departamento_id IN (
    SELECT id
    FROM departamentos
    WHERE nombre = 'Tecnología'
);