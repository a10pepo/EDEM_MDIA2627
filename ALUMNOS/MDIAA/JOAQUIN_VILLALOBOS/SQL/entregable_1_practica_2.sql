-- Los empleados que cobran menos que la media.
SELECT empleados.nombre
FROM empleados
WHERE salario < (
    SELECT AVG(salario) FROM empleados 
);

-- El empleado que más cobra, con MAX en la subconsulta.
SELECT empleados.nombre
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados
);

-- Los empleados de Tecnología, buscando su id con una subconsulta por nombre.
SELECT empleados.nombre
FROM empleados
WHERE departamento_id IN (
    SELECT id FROM departamentos WHERE nombre = 'Tecnología'
);