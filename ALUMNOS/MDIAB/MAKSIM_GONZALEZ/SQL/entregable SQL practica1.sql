Select departamento_id from empleados where nombre='Sara';


SELECT *
FROM empleados
INNER JOIN departamentos
    ON empleados.departamento_id = departamentos.id;

SELECT *
FROM empleados
LEFT JOIN departamentos
    ON empleados.departamento_id = departamentos.id
WHERE empleados.departamento_id IS NULL;