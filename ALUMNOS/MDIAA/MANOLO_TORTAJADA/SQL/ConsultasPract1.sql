SELECT nombre, departamento_id AS departamento 
FROM empleados
WHERE nombre = 'Sara'
    AND departamento_id IS NULL

SELECT E.nombre, D.nombre
FROM empleados E
INNER JOIN departamentos D ON E.departamento_id = D.id
--No sale Sara