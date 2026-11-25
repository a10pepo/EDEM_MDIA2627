-- Query para ver que empleados cobran menos que la media
SELECT nombre 
FROM empleados
WHERE salario < (SELECT AVG(salario) FROM empleados);

-- Empleados que cobra mas
SELECT nombre 
FROM empleados
WHERE salario = (SELECT MAX(salario) FROM empleados);

-- Seleccionar empleados que pertenecen al departamento de tecnología
select nombre,email,salario,departamentos.nombre_departamento
FROM empleados
LEFT JOIN departamentos ON empleados.id_departamento = departamentos.id
WHERE id_departamento = (SELECT id FROM departamentos WHERE nombre_departamento = 'Tecnología');

