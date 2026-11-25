# Equipo 5 · Suscripción

Terra Taronja quiere probar un servicio de entregas periódicas. Comparad cómo compran los clientes particulares en dos provincias y proponed dónde empezar. Escribid las consultas en el [archivo de trabajo](./consultas.sql).

## Paso 1 · Contad pedidos y clientes

En **Explorer**, abrid `terra_taronja_raw.orders` y mirad **Preview**. Cada fila representa un pedido.

1. Elegid dos provincias con pedidos. Filtrad `province`, `customer_type` con valor `particular` y `order_date` para quedaros con 2025.
2. Agrupad por provincia. Usad `COUNT(*)` para contar pedidos y `COUNT(DISTINCT customer_id)` para contar clientes distintos.
3. Dividid los pedidos entre los clientes distintos para obtener la media de pedidos por cliente.

Esto responde a las preguntas 1 a 3.

## Paso 2 · Buscad compras en meses distintos

Para la pregunta 4, conservad las mismas provincias, el tipo de cliente y el año.

1. Usad `DATE_TRUNC(order_date, MONTH)` para obtener el mes de cada pedido. Agrupad primero por provincia y cliente y contad sus meses distintos.
2. Quedaos con los clientes que compraron en **dos meses o más**. Contad cuántos hay en cada provincia.

Dos compras en enero cuentan como **un mes**. Una en enero y otra en febrero cuentan como **dos meses**.

## Paso 3 · Elegid dónde probar

Para la pregunta 5, usad los pedidos por cliente y el número de clientes que compraron en varios meses para justificar vuestra elección. Pensad qué comprobaríais con una prueba pequeña, como si los clientes aceptarían un envío con una frecuencia fija.

## Si os queda tiempo

Dividid los clientes que compraron en al menos dos meses entre **todos los particulares que compraron en 2025** en la misma provincia. Multiplicad por 100. Si 20 de 100 clientes compraron en varios meses, la proporción es del **20 %**. Comparad los porcentajes de las dos provincias y revisad si eso cambia vuestra recomendación.
