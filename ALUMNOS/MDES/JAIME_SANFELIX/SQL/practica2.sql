SELECT nombre, salario FROM empleados WHERE salario < (SELECT AVG(salario) FROM empleados);
SELECT nombre, salario FROM empleados WHERE salario = (SELECT MAX(salario) FROM empleados);
SELECT empleados.nombre FROM empleados
WHERE empleados.departamento_id IN
(SELECT departamentos.id FROM departamentos WHERE departamentos.nombre = 'Tecnología');