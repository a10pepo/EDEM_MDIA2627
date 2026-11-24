SELECT nombre 
FROM empleados
WHERE salario < (SELECT AVG(salario)
                FROM empleados)

SELECT nombre 
FROM empleados
WHERE salario = (SELECT MAX(salario)
                FROM empleados)
                
SELECT nombre 
FROM empleados
WHERE departamento_id = (SELECT id
                        FROM departamentos
                        WHERE nombre = 'Tecnología')