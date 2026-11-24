SELECT nombre
FROM empleado
WHERE salario < (SELECT AVG(salario) FROM empleado);


SELECT nombre
FROM empleado
WHERE salario = (SELECT MAX(salario) FROM empleado);

select nombre 
from empleado 
where departamento_id = (select id_dpt from departamento where nombre = 'Tecnología');