# Soluciones del ejercicio final · Terra Taronja

El [enunciado del alumno](../README.md) plantea cinco decisiones. Abre el `consultas.sql` del equipo, sustituye `PROJECT_ID` por el ID de tu proyecto y usa `terra_taronja_raw` en **EU**. Ejecuta cada consulta por separado. Algunos bloques devuelven las cifras para varias preguntas seguidas.

Las cifras de referencia corresponden a la semilla **27182** y los **1.200.000 pedidos** del conjunto completo. Se calcularon localmente con SQLite adaptando los nombres de tabla y las funciones de fecha de GoogleSQL. Las provincias y categorías elegidas son ejemplos. Si un equipo elige otras, comprueba que compara el mismo periodo y que las cifras apoyan su propuesta.

## Plantillas resueltas por equipo

Cada equipo tiene un solo `consultas.sql`. La primera parte reproduce las preguntas del alumno en el mismo orden. **Resultado esperado** muestra la cifra de referencia o una respuesta posible cuando la pregunta pide una decisión. **Por qué** explica el cálculo o la decisión. Al final del archivo, **Ampliación para la puesta en común** reúne los bloques docentes que se comentan en esta guía.

| Equipo | Consultas y soluciones |
| --- | --- |
| 1 · Proveedores | [Solución del equipo 1](./equipo_1_proveedores/consultas.sql) |
| 2 · Territorios | [Solución del equipo 2](./equipo_2_territorios/consultas.sql) |
| 3 · Categorías | [Solución del equipo 3](./equipo_3_categorias/consultas.sql) |
| 4 · Canal B2B | [Solución del equipo 4](./equipo_4_b2b/consultas.sql) |
| 5 · Suscripción | [Solución del equipo 5](./equipo_5_suscripcion/consultas.sql) |

## A. Nuevos proveedores

### Consultas sencillas

Abre la [solución del equipo 1](./equipo_1_proveedores/consultas.sql) para seguir las preguntas del alumno.

1. **Por producto.** La naranja de Carcaixent encabeza la lista con **68.858 unidades sin servir** y un **87,54 %** de cumplimiento. Para enseñar por qué conviene mirar ambas medidas, la Caja de cítricos de la Ribera tiene menos unidades sin servir que la Mandarina de Nules (**34.762** frente a **46.307**) y un cumplimiento algo menor (**89,14 %** frente a **89,61 %**).
2. **Por mes.** La brecha de la naranja aparece en los **12 meses**. Marzo concentra **17.383 unidades sin servir**. Esto permite distinguir la recurrencia de un pico aislado.
3. **Por proveedor, opcional.** Para esa naranja, Horta i Camp tiene **64.188 unidades sin servir** y un cumplimiento del **85,70 %**. La Cooperativa del Xúquer tiene **4.670** y un **95,50 %**. El desglose sitúa la brecha, pero para entender su causa haría falta revisar lo acordado y el volumen que podía asumir cada proveedor.

En la reflexión final, pide una recomendación basada en el volumen, el porcentaje y la recurrencia. `requested_units` mide unidades solicitadas para aprovisionamiento. Para afirmar que hubo ventas perdidas o demanda final sin atender harían falta datos de pedidos que la tienda no pudo atender.

### Consulta avanzada

Ejecuta el bloque 5 de la ampliación del equipo 1.

**Qué obtenemos.** Una fila por producto y proveedor en 2025. Cruzamos las ventas con los registros mensuales de suministro para calcular qué parte de las unidades vendidas de cada producto pasan por cada proveedor, qué fracción de las unidades solicitadas para aprovisionamiento quedó sin servir, qué se recibió frente al plan y cuántos meses hubo roturas.

**Por qué.** Un producto con muchas ventas puede tener muchas incidencias simplemente por su volumen. La proporción sin servir, la dependencia de un proveedor y la repetición de las roturas permiten distinguir los casos en que diversificar el suministro aportaría valor.

**Qué sacamos de ahí.** Horta i Camp sirve cerca del **80 %** de la naranja de Carcaixent vendida, deja sin cubrir unas **64.200 unidades** solicitadas y registra alrededor del **24 %** de expediciones tardías para ese producto. La coincidencia de concentración y problemas repetidos hace que sea un caso prioritario. Hay proveedores por encima del **94 %** de recepción sobre plan y por debajo del **9 %** de retrasos. En la naranja el peor mes llega a 12 días de rotura.

**Para qué sirve.** Priorizar la búsqueda de un proveedor valenciano adicional para los productos que combinan concentración y problemas persistentes. Comprobar primero la capacidad de los proveedores secundarios actuales. En estos datos sintéticos, las unidades servidas y vendidas coinciden por construcción.

## B. Expansión territorial

### Consultas sencillas

Abre la [solución del equipo 2](./equipo_2_territorios/consultas.sql). La primera consulta identifica los pilotos y resume su duración y cobertura. La segunda calcula los pedidos totales, los pedidos por mes y el envío medio a partir de los pedidos de cada provincia en sus meses piloto. El plazo de entrega es opcional y se calcula sobre los mismos pedidos.

| Provincia | Meses de piloto | Cobertura media | Pedidos durante el piloto | Pedidos por mes | Envío medio | Entrega media |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A Coruña | 12 | 47,42 % | 34.428 | 2.869 | 7,43 € | 2,71 días |
| Santa Cruz de Tenerife | 11 | 35,73 % | 22.446 | 2.040,55 | 13,73 € | 5,94 días |

Los pedidos por mes usan todos los meses de piloto como denominador, incluso si algún mes no hubo pedidos. En este ejemplo, A Coruña combina más pedidos por mes y un coste medio de envío menor. Su cobertura también es mayor. Conviene tenerla en cuenta antes de extrapolar los resultados a toda la provincia. El menor plazo medio de entrega refuerza la propuesta de ampliar primero A Coruña.

### Consulta avanzada

Ejecuta el bloque 5 de la ampliación del equipo 2.

**Qué obtenemos.** Resultados por provincia piloto y por comunidad con primeras compras por contacto cualificado, repetición, logística y contribución sobre ventas netas. Los pedidos y costes corresponden a meses de piloto. Para la repetición se toma a quienes hicieron su primera compra en uno de esos meses y se les sigue durante 90 días completos.

**Por qué.** El número de pedidos depende en parte del alcance del piloto. Relacionarlo con la exposición y comprobar si los clientes vuelven permite evaluar el interés observado. El coste y el plazo de entrega ayudan a valorar si ampliar la cobertura sería viable.

| Piloto en 2025 | Pedidos | Primeras compras por contacto | Repiten en 90 días | Envío medio | Entrega media | Contribución sobre neto |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Galicia · cuatro provincias | 92.117 | 8,4 % | 65,0 % | 7,62 € | 2,72 días | 25,9 % |
| Canarias · dos provincias | 44.666 | 7,7 % | 60,7 % | 13,24 € | 5,94 días | 21,3 % |
| Cataluña · Girona | 16.051 | 9,2 % | 50,2 % | 8,19 € | 2,71 días | 25,0 % |

**Qué sacamos de ahí.** Galicia combina repetición alta, coste de envío moderado y buena contribución. Canarias también muestra repetición y contribución positiva, con envíos más caros y lentos. Girona ilustra cómo un cociente inicial alto puede coexistir con menor repetición.

**Para qué sirve.** Ampliar primero el piloto de **Galicia** y mantener **Canarias** como segundo piloto con objetivos de coste y plazo. Los contactos son una estimación agregada simulada. Para medir conversión real habría que enlazar cada contacto con una compra. Una provincia sin operación necesitaría evidencia propia.

## C. Nuevas categorías

### Consultas sencillas

Abre la [solución del equipo 3](./equipo_3_categorias/consultas.sql). Dulces artesanos fue la última categoría en incorporarse, en septiembre de 2025. Si se compara con Despensa, el periodo común va de septiembre a diciembre.

| Categoría | Pedidos en el periodo común | Productos en catálogo al cierre |
| --- | ---: | ---: |
| Dulces artesanos | 54.223 | 3 |
| Despensa | 118.421 | 4 |

Contamos pedidos distintos dentro de cada categoría y consultamos el tamaño del catálogo directamente en `products`. Despensa tenía una referencia más y, por tanto, más oportunidades de aparecer en un pedido. La decisión de ampliar Dulces artesanos requiere revisar margen, devoluciones y ventas fuera de Navidad.

La ampliación mensual muestra que Dulces artesanos pasa de **6.395 pedidos en septiembre** a **20.072 en diciembre**. Sirve para preguntar si ese crecimiento continuaría fuera de la campaña navideña.

### Consulta avanzada

Ejecuta el bloque 6 de la ampliación del equipo 3.

**Qué obtenemos.** Una fila por mes y categoría en la ventana común. A los pedidos, descuentos y devoluciones se añaden la fecha de lanzamiento, la proporción de pedidos en campaña y el margen de producto antes de logística y servicio.

**Por qué.** Un catálogo recién lanzado ha tenido menos tiempo para acumular pedidos. Comparar los mismos meses y revisar descuentos, devoluciones y margen permite valorar si el crecimiento se traduce en mejores resultados económicos.

**Qué sacamos de ahí.** **Dulces artesanos** pasa de **6.395** a **20.072** pedidos entre septiembre y diciembre, con un margen de producto cercano al **43 %**. El periodo observado incluye Navidad. En diciembre **Conservas vegetales** alcanza **20.837** pedidos y tiene cerca del **15 %** de descuento sobre bruto, **3,1 %** de unidades devueltas y **22 %** de margen de producto. Despensa registra **30.781** pedidos, alrededor del **38 %** de margen y **0,4 %** de devoluciones.

**Para qué sirve.** Prolongar las pruebas por categoría antes de ampliar el catálogo en general. Observar Dulces fuera de Navidad y probar Conservas con otros descuentos o combinaciones de productos. La campaña se registra a nivel de pedido. Haría falta una comparación controlada para atribuirle el cambio de volumen.

## D. Canal B2B

### Consultas sencillas

Abre la [solución del equipo 4](./equipo_4_b2b/consultas.sql). La primera consulta compara pedidos e importe neto medio. La consulta opcional añade el coste de servicio y la contribución sobre ventas netas.

1. **Pedidos y cesta.** Las grandes empresas hacen **8.772 pedidos** con un importe neto medio de **411,48 €**. Los restaurantes hacen **140.176 pedidos** con una media de **93,97 €**. Las cifras distinguen el tamaño de cada compra del volumen del segmento.
2. **Costes y contribución.** El coste de servicio por pedido es de **1,89 €** en restaurantes y **22,43 €** en grandes empresas. La contribución sobre ventas netas es del **28,9 %** y del **10,9 %**, respectivamente. Sirve para comparar cuánto queda por cada euro vendido.

### Consulta avanzada

Ejecuta el bloque 6 de la ampliación del equipo 4.

**Qué obtenemos.** Una fila por segmento con sus métricas económicas de 2025, su frecuencia en los 90 días posteriores a la primera compra y la proporción de clientes que supera distintos umbrales de contribución. La duración del seguimiento es la misma para los tres segmentos.

**Por qué.** El corte anual mide cuánto aporta cada segmento al negocio. Los 90 días desde la primera compra permiten comparar el ritmo de clientes que empezaron en fechas distintas. Juntas, ambas medidas ayudan a decidir si una cesta grande justifica un canal dedicado.

| Segmento | Pedidos en 90 días | Cesta neta media | Servicio por pedido | Contribución sobre neto |
| --- | ---: | ---: | ---: | ---: |
| Particular | 2,54 | 33,96 € | 0,90 € | 30,3 % |
| Pequeño restaurante | 5,98 | 93,97 € | 1,89 € | 28,9 % |
| Gran empresa | 2,01 | 411,48 € | 22,43 € | 10,9 % |

**Qué sacamos de ahí.** Las grandes empresas tienen la cesta media más alta y también el mayor coste de servicio por pedido. Los pequeños restaurantes compran más veces en su primera ventana de 90 días y conservan más contribución por euro neto. Más del **22 %** de las grandes cuentas activas supera el **20 %** de contribución sobre neto, así que dentro del segmento hay contratos atractivos.

**Para qué sirve.** Probar un canal para pequeños restaurantes y evaluar contratos grandes individualmente. Antes de comprometerse con un canal dedicado, estimar sus costes fijos y de captación.

## E. Suscripción

### Consultas sencillas

Abre la [solución del equipo 5](./equipo_5_suscripcion/consultas.sql). La primera consulta compara pedidos y clientes particulares en 2025. La segunda cuenta cuántos clientes compraron en dos meses distintos o más.

| Provincia | Pedidos de particulares | Clientes distintos | Pedidos por cliente | Clientes con compras en dos meses o más | Porcentaje opcional |
| --- | ---: | ---: | ---: | ---: | ---: |
| Valencia | 94.023 | 27.388 | 3,43 | 17.202 | 62,81 % |
| Girona | 11.624 | 5.547 | 2,10 | 2.441 | 44,01 % |

La media de pedidos y el número de clientes con compras en varios meses apoyan probar primero en Valencia. El porcentaje también favorece a Valencia al tener en cuenta el distinto tamaño de las dos bases de clientes. El denominador incluye a todos los clientes particulares que compraron en 2025 en cada provincia.

### Consulta avanzada

Ejecuta el bloque 5 de la ampliación del equipo 5.

**Qué obtenemos.** Una fila por provincia para particulares de la cohorte 2025 con **90 días** completos de observación. La consulta pide tres intervalos, una media entre 10 y 35 días, variación relativa moderada y al menos un 55 % de coincidencia media con la cesta anterior. Cada coincidencia se calcula sobre los productos de la cesta actual. Los umbrales son un punto de partida para comparar.

**Por qué.** Un grupo de clientes puede comprar con frecuencia y variar mucho las fechas o el contenido del pedido. Para ofrecer una suscripción importa que coincidan el ritmo y el tipo de cesta. Usar toda la cohorte como denominador evita sobreestimar el tamaño del grupo al contar solo a quienes ya repiten.

| Provincia | Clientes elegibles | Repiten en 90 días | Cesta recurrente y regular |
| --- | ---: | ---: | ---: |
| Valencia | 15.662 | 67,7 % | 34,2 % |
| Castellón | 4.768 | 67,6 % | 34,0 % |
| Girona | 3.962 | 44,9 % | 7,9 % |

**Qué sacamos de ahí.** Valencia y Castellón conservan aproximadamente un tercio de la cohorte con ritmo regular y cesta repetida. Girona queda por debajo del 8 % con los mismos criterios. El recorrido básico cuenta meses de compra durante el año. Esta consulta usa el mismo seguimiento de 90 días para cada cliente y añade regularidad y similitud de la cesta.

**Para qué sirve.** Elegir Valencia o Castellón para un primer piloto. Probar otros umbrales y comprobar si el patrón persiste fuera de campañas. Una prueba comercial permitiría medir la disposición a suscribirse, la frecuencia elegida y el margen del servicio.

## Convenciones de los datos

Cada importe se guarda en céntimos. El bruto suma cantidad × precio unitario. El neto descuenta descuentos y reembolsos. El coste de producto se calcula sobre unidades expedidas, incluidas las devueltas, como aproximación conservadora sin recuperación de mercancía. Los pedidos se fechan entre 2023 y 2025. Alguna entrega ocurre en enero de 2026 cuando el pedido se realiza a final de año.
