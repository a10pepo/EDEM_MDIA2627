# BigQuery · Ejercicio final · Cinco decisiones para Terra Taronja

Terra Taronja vende exclusivamente productos valencianos. Usad su histórico de ventas, suministro y entregas para presentar cinco decisiones al equipo de la tienda.

## Antes de empezar

- Trabajad con `terra_taronja_raw` en vuestro propio proyecto, en **EU**. Si aún no tenéis el histórico, completad los pasos 1 a 3 del [Lab 2](../lab02/README.md). Si han caducado las tablas del lab, repetid los pasos 2 y 3 con los CSV que ya generasteis.
- En BigQuery Studio, abrid **SQL query**. Usad el **Project ID** de vuestro proyecto en las referencias a las tablas.

## Cómo empezar

Cada equipo trabaja una decisión. El archivo SQL reúne preguntas guía para ir ampliando el análisis. Empezad con el recorrido básico.

1. Abrid en **Explorer** la primera tabla de vuestro equipo. Mirad **Preview** para entender qué representa una fila y **Schema** para localizar las columnas.
2. Seguid las preguntas en orden y usad el periodo que indique cada una. Escribid el SQL debajo de la primera pregunta que resuelva y anotad qué cifras usaríais para responder a las siguientes. Una consulta puede servir para varias preguntas.
3. Preparad una propuesta breve con vuestras cifras, por qué apoyan esa propuesta y qué dato os falta para decidir. Podéis proponer una prueba pequeña o pedir más información.

Cuando tengáis eso, podéis continuar con las preguntas bajo «¿Qué podéis mirar si os queda tiempo?». En Proveedores, el desglose por proveedor es opcional. Responded a la reflexión final aunque saltéis ese desglose.

## Equipos y decisiones

1. [Equipo 1 · Proveedores](./equipo_1_proveedores/consultas.sql). ¿Hay productos para los que convenga incorporar proveedores?
2. [Equipo 2 · Territorios](./equipo_2_territorios/consultas.sql). ¿En qué territorios merece la pena ampliar la cobertura?
3. [Equipo 3 · Categorías](./equipo_3_categorias/consultas.sql). ¿Qué haríais con las categorías recién lanzadas?
4. [Equipo 4 · Canal B2B](./equipo_4_b2b/consultas.sql). ¿Qué tipo de cliente justifica probar un canal B2B?
5. [Equipo 5 · Suscripción](./equipo_5_suscripcion/consultas.sql). ¿Dónde probaríais una suscripción?

| Equipo | Primer paso | Si os queda tiempo |
| --- | --- | --- |
| 1 · Proveedores | En `supplier_monthly`, comparad `requested_units` y `fulfilled_units` por `product_id`. Calculad el porcentaje servido y revisad los meses del producto con la mayor diferencia. | Comparad el cumplimiento de los proveedores de ese producto. |
| 2 · Territorios | Seguid la [guía paso a paso](./equipo_2_territorios/README.md). Elegid dos provincias y comparad sus pedidos por mes de piloto y el coste medio de envío durante la prueba. | Comparad cuánto tardaron en llegar esos pedidos. |
| 3 · Categorías | Seguid la [guía paso a paso](./equipo_3_categorias/README.md). Comparad los pedidos de dos categorías durante los mismos meses y tened en cuenta cuántos productos tenía cada una. | Mirad cómo evolucionaron los pedidos de ambas categorías mes a mes. |
| 4 · Canal B2B | En `orders`, comparad número de pedidos e importe neto medio de restaurantes y grandes empresas. B2B significa vender a otros negocios. | Comparad cuánto cuesta atender un pedido de cada grupo. |
| 5 · Suscripción | Seguid la [guía paso a paso](./equipo_5_suscripcion/README.md). Comparad pedidos por cliente y cuántos particulares compraron en dos meses o más en cada provincia. | Calculad qué porcentaje representan esos clientes y revisad vuestra propuesta. |

## Qué contiene cada tabla

| Tabla | Qué representa cada fila |
| --- | --- |
| `customers` | Cliente con nombre de contacto y correo sintéticos, segmento, destino, alta y primera compra |
| `orders` | Pedido con fecha, campaña, entrega, ingresos y costes |
| `order_items` | Línea de pedido con producto, proveedor, precio, coste y devolución |
| `products` | Producto valenciano con categoría, origen y fecha de alta en el catálogo |
| `suppliers` | Proveedor valenciano y su provincia |
| `supplier_monthly` | Producto, proveedor y mes con unidades solicitadas para aprovisionamiento, unidades servidas y logística |
| `territory_monthly` | Provincia y mes con tipo de programa comercial y porcentaje de cobertura |

`province` en pedidos y clientes es el **destino**. El origen del alimento está en `products.origin_province`. Los importes en `_cents` están en céntimos. El neto del pedido descuenta promociones y devoluciones del bruto. La contribución añade los portes cobrados y resta el coste del producto, del envío y del servicio. La contribución todavía no descuenta costes fijos.

Para **Proveedores**, el porcentaje de cumplimiento se calcula dividiendo el total servido entre el total solicitado y multiplicando por 100. Por ejemplo, si se sirvieron 80 de 100 unidades, el cumplimiento fue del **80 %**. Las unidades solicitadas en `requested_units` corresponden al aprovisionamiento. Para saber si quedaron clientes sin atender o se perdieron ventas harían falta datos sobre esos pedidos.

Los datos cubren el histórico disponible hasta el 31 de diciembre de 2025. La [guía de Territorios](./equipo_2_territorios/README.md) explica qué son los pilotos y la cobertura.

## Soluciones

Después de resolver el ejercicio, podéis contrastar las cifras y la decisión de cada equipo con los [resultados de referencia](./solucion/RESULTADOS.md).

## Limpieza

Una vez entregado el ejercicio, sigue la [limpieza de datasets del Lab 2](../lab02/README.md#limpieza).
