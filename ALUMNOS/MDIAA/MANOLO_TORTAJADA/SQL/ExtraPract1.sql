SELECT *
FROM empleados E
INNER JOIN departamentos D ON E.departamento_id = D.id
-- Me va a salir lo mismo que en la consulta de la pract.
-- Todos los empleados y el departamento al que están asociados
-- Si el empleado no tiene un departamento asociado no sale

SELECT *
FROM empleados E
LEFT JOIN departamentos D ON E.departamento_id = D.id
-- Todos los empleados y el departamento al que están asociados 
-- Estén asociados a un departamento o no

SELECT *
FROM empleados E
FULL OUTER JOIN departamentos D ON E.departamento_id = D.id
-- Todos los empleados y todos los departamentos
-- Tanto si hay un departamento asociado al empleado o no
-- Tanto si hay empleados en un departamento como si no


SELECT nombre
FROM empleados 
WHERE departamento_id IS NULL

SELECT D.nombre
FROM departamentos D
LEFT JOIN empleados E ON d.ID = E.departamento_id
WHERE E.nombre IS NULL