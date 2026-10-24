-- Empleados que cobran menos que la media
SELECT *
FROM empleados
WHERE salario < (
    SELECT AVG(salario)
    FROM empleados
);

-- El empleado que más cobra
SELECT *
FROM empleados
WHERE salario = (
    SELECT MAX(salario)
    FROM empleados
)

-- Los empleados de "Tecnología", buscando su is con una subconsulta por nombre
SELECT *
FROM empleados
WHERE departamento_id IN (
    SELECT id
    FROM departamentos
    WHERE nombre_departamento = 'Tecnología' 
);