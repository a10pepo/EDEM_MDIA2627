-- Los empleados que cobran menos que la media.

SELECT *
FROM empleados
WHERE salario < (
    SELECT AVG(salario)
    FROM empleados
);

-- El empleado que más cobra, con MAX en la subconsulta.

SELECT *
FROM empleados
WHERE salario = (
    SELECT MAX(salario)
    FROM empleados
);

-- Los empleados de Tecnología, buscando su id con una subconsulta por nombre.

SELECT *
FROM empleados
WHERE departamento_id = (
    SELECT id
    FROM departamentos
    WHERE nombre = 'Tecnología'
);