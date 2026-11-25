# Equipo 3 · Categorías

Terra Taronja ha incorporado una categoría al catálogo. Vais a compararla con otra para decidir si conviene añadir más productos. Escribid vuestras consultas en el [archivo de trabajo](./consultas.sql).

## Paso 1 · Elegid las categorías y los meses

En **Explorer**, abrid `terra_taronja_raw.products` y mirad **Preview**. Cada fila es un producto. La columna `catalog_since` indica cuándo entró en el catálogo.

1. Buscad la primera fecha de `catalog_since` de cada `category` con `MIN`.
2. Identificad la categoría que empezó más tarde y elegid otra para compararla. La fecha de entrada de la más reciente fija el inicio del periodo común. Terminad en diciembre de 2025, el último mes de los datos.

Esto responde a las preguntas 1 a 3.

## Paso 2 · Comparad pedidos y productos

1. Para los pedidos, relacionad `orders` con `order_items` por `order_id`. Relacionad `order_items` con `products` por `product_id` para saber la categoría de cada línea.
2. Filtrad por las dos categorías y por el periodo común con `orders.order_date`. Agrupad por categoría y usad `COUNT(DISTINCT order_id)`. Si un pedido lleva dos productos de la misma categoría, contadlo una vez en esa categoría. Si contiene productos de ambas, puede aparecer una vez en cada grupo.
3. Para saber cuántos productos tenía cada categoría, volved a `products`. Contad los productos que ya estaban en el catálogo al cierre del periodo, incluso si alguno no aparece en ningún pedido.

Esto responde a las preguntas 4 y 5. Una categoría con más productos tiene más oportunidades de aparecer en un pedido. Tened en cuenta el tamaño del catálogo al comparar los totales.

## Paso 3 · Defended una decisión

Para la pregunta 6, decidid si esas cifras os bastan para recomendar más productos en la categoría reciente. Si os falta información, indicad qué miraríais antes de decidir, como el margen, las devoluciones o si las ventas se mantienen fuera de campaña.

## Si os queda tiempo

Repetid el recuento de pedidos agrupando también por mes con `DATE_TRUNC(order_date, MONTH)`. Mirad si el volumen se mantiene o si se concentra en un mes.
