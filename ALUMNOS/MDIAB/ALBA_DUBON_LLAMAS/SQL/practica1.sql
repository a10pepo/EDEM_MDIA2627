create table departamento (
    id_dpt INT generated ALWAYS AS IDENTITY primary key,
    nombre varchar(50) not null

);


create table empleado (
    id_emp INT generated ALWAYS AS IDENTITY primary key,
    nombre varchar (100) not NULL,
    email varchar(100) not null,
    salario int not NULL,
    departamento_id INTEGER references departamento(id_dpt)

);

CREATE table proyecto (
    id_pro INT generated ALWAYS AS IDENTITY primary key,
    nombre varchar(150) not NULL,
    fec_ini date not NULL,
    departamento_id INTEGER references departamento(id_dpt)
);


INSERT INTO departamento (nombre) VALUES
    ('Ventas'), ('Tecnología'), ('Legal'), ('I+D');


INSERT INTO empleado
    (nombre, email, salario, departamento_id)
VALUES
    ('Ana',   'ana@empresa.com',   52000, 2),
    ('Luis',  'luis@empresa.com',  38000, 2),
    ('Marta', 'marta@empresa.com', 45000, 1),
    ('Pablo', 'pablo@empresa.com', 31000, 1),
    ('Sara',  'sara@empresa.com',  29000, NULL);




select empleado.nombre from empleado
left join departamento
on empleado.departamento_id = departamento.id_dpt
where empleado.departamento_id is null;

select empleado.nombre, empleado.departamento_id 
from empleado
inner join departamento
on empleado.departamento_id = departamento.id_dpt;

