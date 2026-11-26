# Equipo 2 · Territorios

Terra Taronja quiere decidir dónde extender sus ventas. Vuestro primer objetivo es entender **dónde ha probado vender** y **cuánto le cuesta atender los pedidos**.

## Qué significan los datos

- Un **piloto** es una prueba de venta y reparto en una parte de la provincia durante un tiempo. La tienda observa cómo funciona antes de ampliar el servicio. En `sales_program`, estas pruebas aparecen como `piloto`.
- La **cobertura** es la parte de la provincia que abarca el programa comercial en ese mes. En el lab, `coverage_pct` es un porcentaje simulado. Si una provincia tuviera diez zonas comparables y el piloto llegara a cuatro, su cobertura sería del **40 %**. Ese porcentaje describe el alcance de la prueba. Los pedidos se cuentan aparte.

## Paso 1 · Localizad los pilotos

En **Explorer**, abrid `terra_taronja_raw.territory_monthly`. Mirad **Preview** para ver una fila y **Schema** para localizar las columnas. Cada fila corresponde a **una provincia y un mes**.

1. Quedaos con los registros de 2025 en los que `sales_program` vale `piloto`. La fecha del mes está en `month_start`.
2. Usad `GROUP BY` para obtener una fila por `province`. Contad las filas con `COUNT(*)` para saber cuántos meses aparece el piloto y usad `AVG` para sacar la media de `coverage_pct`.
3. Elegid dos provincias piloto y anotad sus meses y su cobertura media. Si una provincia aparece en marzo con un 40 % y en abril con un 60 %, son **2 meses** y la cobertura media es del **50 %**.

Con esto podéis responder a las **dos primeras preguntas** de vuestro [archivo de trabajo](./consultas.sql).

## Paso 2 · Comparad los pedidos y el coste de envío

Ahora abrid `terra_taronja_raw.orders`. Cada fila corresponde a **un pedido**.

1. Partid de la lista de meses de piloto de las dos provincias elegidas. Buscad los pedidos de la misma `province` y del mismo mes. `DATE_TRUNC(order_date, MONTH)` convierte la fecha del pedido al primer día de su mes, igual que `month_start`. Si hubo piloto en marzo y mayo, un pedido de abril queda fuera.
2. Usad `LEFT JOIN` desde la lista de pilotos para conservar también los meses en los que no hubo ningún pedido. Agrupad por provincia y contad los `order_id` para obtener los pedidos. Dividid ese total entre los meses de piloto que contasteis en el paso 1.
3. Calculad la media de `shipping_cost_cents` de los mismos pedidos. Dividid entre 100 para expresar en euros lo que le costó a la tienda cada envío.

Con esto podéis responder a las **preguntas 3 a 5**. Por ejemplo, **120 pedidos en 3 meses** son **40 al mes**. Un piloto con **100 pedidos en 2 meses** consiguió **50 al mes**. El segundo tuvo más pedidos por mes, aunque su total fue menor.

## Paso 3 · Explicad qué haríais

Para la **pregunta 6**, elegid en cuál de las dos provincias ampliaríais la prueba. Comparad los pedidos por mes y el coste de envío. Tened en cuenta también la cobertura, porque los pilotos pueden abarcar partes distintas de cada provincia. Podéis proponer mantener el piloto si os falta información para decidir.

Podéis usar esta frase de partida.

> Comparamos ___ con ___. La primera consiguió ___ pedidos por mes de piloto y su envío medio costó ___ €. Probaríamos ___ porque ___. Antes comprobaríamos ___.

## Si os queda tiempo

Usad los mismos pedidos del paso 2. Para cada pedido, calculad cuántos días hay entre `order_date` y `delivery_date`. Comparad la media en cada provincia y revisad si eso cambia vuestra propuesta.
