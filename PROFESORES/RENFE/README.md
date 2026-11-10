# RENFE — Alerta de proximidad entre trenes

## Descripción

En este ejercicio construiremos un pipeline para capturar y analizar las posiciones GPS de trenes de Alta Velocidad, Larga Distancia y Media Distancia de Renfe. El sistema permitirá configurar una distancia mínima y generará una alerta cuando dos trenes distintos estén a menos de ese valor.

La fuente publica posiciones en tiempo real y se actualiza aproximadamente cada 15 segundos. El conjunto incluye recursos JSON y Protocol Buffers; para el ejercicio comenzaremos con JSON.

- [Conjunto de datos: Posición vehículos AV, LD y MD](https://data.renfe.com/dataset/posicion-vehiculos-av-ld-md)
- Recurso JSON: <https://gtfsrt.renfe.com/vehicle_positions_LD.json>
- Recurso Protocol Buffers: <https://gtfsrt.renfe.com/vehicle_positions_LD.pb>

La disponibilidad y el esquema exacto del recurso pueden cambiar. El alumnado deberá inspeccionar la respuesta actual y adaptar el parser a sus campos. Si el recurso requiere cabeceras, formato o una ruta alternativa, documentar ese ajuste en el proyecto.

## Instrucciones

- Todo el código debe estar en Python.
- Los servicios y scripts se deben poder ejecutar con Docker Compose.
- No se deben guardar credenciales ni datos sensibles en el repositorio.
- Configurar el umbral de proximidad mediante una variable de entorno, por ejemplo `ALERT_DISTANCE_METERS`.
- La distancia entre coordenadas se calculará en metros con una fórmula geodésica como Haversine.
- Cada tren se debe comparar una sola vez con los demás en cada lectura. No generar una alerta al comparar un tren consigo mismo.
- Incluir en cada alerta la identificación disponible de ambos trenes, sus coordenadas, la distancia calculada y la hora de captura.
- La alerta se produce solo cuando la distancia es estrictamente menor que el umbral configurado.
- Tener en cuenta que las posiciones son datos operativos orientativos y pueden tener retraso o imprecisión GPS. El ejercicio no debe presentar las alertas como un sistema de seguridad ferroviaria.

## Objetivos

1. Consumir una API de datos abiertos en tiempo real.
2. Inspeccionar y validar datos JSON externos.
3. Diseñar un pipeline de captura y almacenamiento.
4. Calcular distancias geográficas y aplicar una regla configurable.
5. Visualizar posiciones y alertas en un dashboard.
6. Ejecutar los componentes de forma reproducible con Docker Compose.

## Fase 1: inspección de la fuente y captura

Crear `renfe_collector.py` para consultar periódicamente el recurso JSON. Como la fuente anuncia actualizaciones cada 15 segundos, se recomienda no consultar más rápido que esa frecuencia.

El parser debe extraer, cuando estén disponibles:

- Identificador o matrícula del vehículo
- Latitud y longitud
- Ruta, línea o servicio
- Identificador del viaje
- Fecha/hora de la posición
- Fecha/hora de recepción por el colector

El formato del feed puede seguir GTFS Realtime y cambiar. Validar campos ausentes, coordenadas fuera de rango, respuestas vacías, errores HTTP y registros duplicados. Conservar un ejemplo anonimizado de respuesta para facilitar el desarrollo sin conexión.

## Fase 2: almacenamiento SQL

Almacenar las observaciones sin perder el historial. Propuesta inicial de tabla:

```sql
CREATE TABLE train_positions (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id TEXT NOT NULL,
    trip_id TEXT,
    route_id TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    position_timestamp TIMESTAMPTZ,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    raw_payload JSONB
);
```

Añadir índices adecuados para consultar las posiciones más recientes por vehículo. Documentar las decisiones de deduplicación y los tipos de fecha/hora.

## Fase 3: regla de proximidad y alertas

Crear un componente que lea las posiciones más recientes de los trenes y evalúe cada pareja única.

Requisitos:

- Aceptar el umbral en metros mediante `ALERT_DISTANCE_METERS`.
- Calcular distancia geodésica entre cada pareja de vehículos.
- Generar una alerta si `distancia < ALERT_DISTANCE_METERS`.
- Ignorar posiciones antiguas con una ventana temporal configurable, para evitar comparar datos desfasados.
- Evitar emitir la misma alerta repetidamente en cada ciclo. Definir una estrategia, por ejemplo, emitir solo al entrar en proximidad y volver a notificar después de que la pareja supere el umbral.
- Registrar alertas con vehículos, distancia, coordenadas y marcas temporales.
- Probar casos de umbral, parejas duplicadas, posición faltante y datos desactualizados.

Como ampliación, publicar alertas por consola, webhook o una cola de mensajes.

## Fase 4: transformación con DBT

Configurar DBT para PostgreSQL y crear modelos que preparen las observaciones y alertas para el análisis. Incluir al menos:

- Modelo limpio de posiciones con validación de coordenadas y normalización temporal.
- Modelo de alertas con distancia observada y umbral aplicado.
- Agregados por hora y por pareja de trenes.

Documentar los modelos y añadir pruebas de unicidad, valores no nulos y rangos válidos.

## Fase 5: dashboard

Crear un dashboard que permita:

- Ver posiciones recientes en un mapa, si la herramienta elegida lo permite.
- Consultar alertas por hora, pareja, distancia y servicio.
- Cambiar o mostrar claramente el umbral aplicado.
- Diferenciar datos recientes de posiciones desactualizadas.

## Fase 6: almacenamiento NoSQL (extra)

Ampliar el colector para replicar los eventos o alertas en MongoDB. Explicar qué consultas se benefician de esta copia y cómo se evita duplicar documentos.

## Entregables

- Código Python organizado y documentado.
- `docker-compose.yml` para ejecutar el pipeline.
- Esquema SQL y modelos DBT.
- Dashboard o instrucciones reproducibles para levantarlo.
- `README` con instalación, configuración, ejecución, ejemplo de alerta y limitaciones de los datos.
- Evidencia de una alerta generada con un umbral configurable y datos de ejemplo.
