# RENFE - Alertas de proximidad entre trenes

Ejercicio universitario. Las alertas son **orientativas** y **no** constituyen un
sistema de seguridad ferroviaria.

El colector (`renfe_collector.py`) consulta cada 30 s (la API se actualiza cada 30 s) el estado de la flota de Renfe,
calcula la distancia entre cada par de trenes (Haversine) y genera una alerta si es menor
que el umbral. Posiciones y alertas se guardan en PostgreSQL.

## Regla de alerta

Se genera una alerta entre dos trenes solo si se cumplen **las tres** condiciones:
1. Están en el **mismo tramo A → B**: mismo `codEstAnt` y mismo `codEstSig`, y distintos entre sí
   (un tren con `codEstAnt == codEstSig` está en una estación y no tiene tramo).
2. La distancia (Haversine) es **estrictamente menor** que `ALERT_DISTANCE_METERS`.
3. No son la misma unidad física (no comparten matrícula `mat`).

Los trenes en sentidos contrarios (A y B invertidos) no generan alerta: se asume que van por vías
distintas. Por eso `riesgo_mismo_tramo` es siempre verdadero en las alertas nuevas; el campo se
conserva en la base de datos. Las alertas guardadas antes de este cambio (regla solo por distancia)
pueden tenerlo en falso.

## Arranque con Docker Compose

```
cp .env.example .env        # Windows: copy .env.example .env
# edita .env y cambia POSTGRES_PASSWORD
docker compose up --build
```

Servicios:
- `db`: PostgreSQL 16 con el volumen `pgdata` (los datos sobreviven a `docker compose down`;
  solo `docker compose down -v` los borra).
- `collector`: este proyecto. Espera a que `db` esté sano, crea las tablas (`schema.sql`,
  idempotente) y guarda cada lectura. Si la BD falla, avisa por log y reintenta en el ciclo siguiente.

Consultar los datos:
```
docker compose exec db psql -U renfe -d renfe -c "select * from alerts order by captured_at desc limit 5"
docker compose exec db psql -U renfe -d renfe -c "select * from positions where cod_comercial='18014' order by position_time desc limit 5"
```

### Cambiar el umbral de proximidad

El umbral (en metros) se define en `.env` con `ALERT_DISTANCE_METERS` (por defecto 5000).
Para cambiarlo, edita ese valor y recrea el colector:
```
docker compose up -d collector
```
(Compose detecta el cambio de configuración y reinicia solo el colector; la BD no se toca.)
Solo se genera alerta si la distancia es **estrictamente menor** que el umbral.

### Consultar los logs
```
docker compose logs -f collector        # en directo (Ctrl+C sale sin parar el servicio)
docker compose logs --tail 50 collector # últimas 50 líneas
docker compose logs --since 10m collector
docker compose logs db                  # logs de PostgreSQL
docker compose ps                       # estado de los servicios
```
En el log del colector verás cada lectura (trenes válidos, descartados y alertas) y una línea
`BD: N posiciones nuevas, M alertas nuevas` por ciclo. Los avisos (`WARNING`) indican
posiciones descartadas o fallos de red/BD; el colector sigue funcionando y reintenta.

### Ejecución automática
Un solo comando levanta todo: `docker compose up` (o `up -d` en segundo plano). `db` tiene un
healthcheck y `collector` solo arranca cuando está sano (`depends_on: service_healthy`);
ambos se reinician solos (`restart: unless-stopped`) y el colector captura de forma continua
sin más pasos. Requisito único: tener creado el fichero `.env`.

## API (backend FastAPI)

Servicio `backend` (carpeta `backend/`, contenedor propio). Arranca con el resto de servicios
cuando la BD está sana. Conecta con `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
y lee de la BD en modo solo lectura.

- Swagger (documentación interactiva): <http://localhost:8000/docs>
- Puerto: `BACKEND_PORT` en `.env` (por defecto 8000).

| Endpoint | Descripción | Errores |
|---|---|---|
| `GET /getAlertas?limit=50` | Alertas de más recientes a más antiguas (`limit` 1-1000, defecto 50), con ambos trenes, distancia, umbral y fecha/hora | 422 `limit` inválido; 503 BD |
| `GET /getPosiciones?limit=500` | Última posición de cada tren con muestra más joven que `MAX_POSITION_AGE_SECONDS` (`total`, `ultima_recepcion` y lista de trenes). La usa el frontend | 503 BD |
| `GET /getEstelas?minutos=15` | Posiciones de los últimos `minutos` (1-120) de cada tren, `[lat, lon, epoch]`, para dibujar su estela. La usa el frontend | 503 BD |
| `GET /getTren/{id}` | Datos y posición más recientes del tren (`id` = codComercial, p. ej. `03160`), con su antigüedad y si es reciente | 404 no existe; 503 BD |
| `GET /getDistancia/{trenId1}/{trenId2}` | Distancia actual en metros (Haversine) entre las últimas posiciones de ambos | 400 mismo tren; 404 alguno no existe; 409 posición no reciente; 503 BD |

Una posición es "reciente" si tiene menos de `MAX_POSITION_AGE_SECONDS` (300 s por defecto).
Los errores de BD devuelven 503 (BD caída) o 500 (otro error) con un mensaje genérico; el
detalle va al log (`docker compose logs backend`).

Ejemplos:
```
curl "http://localhost:8000/getAlertas?limit=5"
curl http://localhost:8000/getTren/03160
curl http://localhost:8000/getDistancia/03160/03161
```

## Frontend (fase 6)

Aplicación web estática (HTML + CSS + JavaScript sin librerías) servida por nginx. Todo el stack
arranca con un solo comando: `docker compose up`. Después abre <http://localhost:8080>
(puerto configurable con `FRONTEND_PORT` en `.env`).

### Cómo se conecta (y por qué es seguro)
```
navegador ──> nginx (frontend:80) ──/api/*──> FastAPI (backend:8000) ──> PostgreSQL
```
- El navegador solo habla con nginx. nginx reenvía `/api/...` al backend dentro de la red de Docker
  (`frontend/nginx.conf.template`; la URL del backend es la variable `BACKEND_URL`). No hay CORS
  porque el navegador ve un único origen.
- El navegador **nunca** se conecta a SQL y el código del frontend no contiene credenciales; la
  contraseña de la base de datos solo llega al backend y al colector por variables de entorno.

### Qué muestra
- **Mapa:** el último dato de cada tren (punto) y su **estela** de los últimos 15 minutos (línea), a partir
  de `/api/getEstelas`. Zoom con la rueda, arrastre para mover y botón «Restablecer zoom». Los trenes
  que aparecen en alguna alerta mostrada se pintan en rojo; clic en un tren resalta su estela. Si dos
  muestras seguidas implican más de 350 km/h se considera un salto del dato y **no se unen con una
  línea**, para no dibujar saltos de cientos de kilómetros que no son movimientos reales. La estela
  crece con el tiempo: justo después de arrancar el colector solo hay unos minutos de historial.
- **Tabla de posiciones:** tren, matrícula, latitud, longitud, tramo con **nombre de las estaciones**
  (`frontend/estaciones.json`, sacado del GTFS de Renfe; el código va en el tooltip), retraso y
  antigüedad. Filtro por nº de tren o matrícula.
- **Alertas recientes:** hora (Madrid), **entre qué dos trenes** (con sus matrículas), distancia medida,
  umbral y **por qué hay alerta**: mismo tramo A → B, distancia menor que el umbral y unidades distintas.
  Las alertas guardadas con la regla anterior (solo distancia, `riesgo_mismo_tramo` falso) se marcan
  como tales y explican que los trenes iban en tramos distintos. Clic en una alerta une los dos
  trenes en el mapa con una línea y resalta sus estelas.
- **Resumen:** trenes con posición reciente, alertas mostradas, umbral y hora de la última alerta.

### Actualización y estados
- **Sondeo** cada 15 s (`POLL_MS` en `frontend/app.js`; la fuente se actualiza cada 30 s). Se pausa
  si la pestaña no está visible y se refresca al volver. Cada petición tiene 8 s de timeout.
- **Conectado:** punto verde, "actualizado hace N s" (se refresca cada segundo sin llamar a la API).
- **Sin datos recientes:** punto naranja y aviso si la API responde pero no hay posiciones de menos
  de `MAX_POSITION_AGE_SECONDS`; indica cuándo guardó datos el colector por última vez.
- **Servicio no disponible / sin conexión:** punto rojo y aviso si la API falla (502/503, timeout o
  red). Si ya había datos se conservan en pantalla atenuados con "último dato hace N min"; si no,
  las tablas muestran "Sin conexión con el servicio". Reintenta solo.

### Revisión del código (generado con ayuda de IA)
| Archivo | Qué hace |
|---|---|
| `frontend/index.html` | Estructura de la página: cabecera con estado, banner, resumen, tabla+mapa, alertas |
| `frontend/styles.css` | Estilos con variables CSS y tema claro/oscuro automático |
| `frontend/app.js` | `fetchJSON` (red + timeout), `refresh` (sondeo), `renderStatus`/`render*` (pintado), `trailSegments` (estelas sin saltos), zoom/arrastre y selección |
| `frontend/estaciones.json` | Código de estación → nombre (GTFS estático de Renfe) |
| `frontend/nginx.conf.template` | Sirve los estáticos y hace de proxy `/api/` → backend |
| `frontend/Dockerfile` | Imagen `nginx:alpine` con los archivos; `BACKEND_URL` se inyecta al arrancar |

Decisiones revisadas: el DOM se construye con `textContent` y nunca con `innerHTML` a partir de datos
de la API (evita inyección de HTML); los datos antiguos se conservan al fallar la red en lugar de
vaciar la pantalla; los estados vacío y de error son explícitos; el temporizador de 1 s solo toca
el texto de estado y no reconstruye las tablas. Limitaciones: el mapa no tiene cartografía base
(solo puntos y estelas) y los nombres de estación vienen de un fichero estático que habría que
regenerar si Renfe cambia sus códigos.

### Variables de entorno

Las credenciales viven solo en `.env` (ignorado por git; el repositorio solo contiene `.env.example`).

| Variable | Defecto | Descripción |
|---|---|---|
| `POSTGRES_PASSWORD` | (obligatoria) | Contraseña de la BD; compose no arranca sin ella |
| `POSTGRES_DB` / `POSTGRES_USER` | renfe / renfe | Nombre de BD y usuario |
| `ALERT_DISTANCE_METERS` | 5000 | Umbral en metros (alerta si distancia < umbral) |
| `POLL_INTERVAL_SECONDS` | 30 | Segundos entre consultas (la API se actualiza cada 30 s; mínimo 15) |
| `MAX_POSITION_AGE_SECONDS` | 300 | Se descartan posiciones más antiguas |
| `LOG_LEVEL` | INFO | Nivel de logging |

Dentro del contenedor, el colector recibe la conexión por `DB_HOST`, `DB_PORT`, `DB_NAME`,
`DB_USER` y `DB_PASSWORD` (compose los rellena). Sin `DB_HOST` el colector funciona sin
base de datos, solo por consola. Otras variables del colector: `RENFE_URL`, `SAMPLE_FILE`.

## Modelo de datos (`schema.sql`)

**`positions`**: una fila por posición GPS de un tren.
**`alerts`**: una fila por alerta, con ambos trenes (código, matrícula, lat/lon, A/B, hora de
su posición), distancia observada, umbral, `riesgo_mismo_tramo` y hora de captura.

### Índices
| Índice | Consulta que sirve |
|---|---|
| `positions (cod_comercial, position_time DESC)` (también es la restricción única) | posiciones recientes de un vehículo |
| `positions (received_at DESC)` | últimas posiciones de la flota |
| `alerts (captured_at DESC)` | alertas por fecha |
| `alerts (train_a_cod, captured_at DESC)` y `(train_b_cod, ...)` | historial de alertas de un tren |

### Decisiones de deduplicación
- **Posiciones:** el feed repite la misma posición de un tren en lecturas consecutivas mientras
  su `time` no cambia. La clave `UNIQUE (cod_comercial, position_time)` con
  `ON CONFLICT DO NOTHING` guarda cada muestra GPS una sola vez (en las pruebas, ~15 % de las
  posiciones de cada ciclo eran repetidas). Se usa `time` (hora de la muestra) y no
  `received_at`, que cambiaría en cada lectura.
- **Alertas:** el par se guarda en orden canónico (`train_a_cod < train_b_cod`, forzado con un
  `CHECK`), de modo que (A,B) y (B,A) son la misma alerta. La clave
  `UNIQUE (train_a_cod, train_b_cod, train_a_position_time, train_b_position_time)` evita
  repetir la alerta cuando ninguno de los dos trenes ha enviado posición nueva. Si cualquiera
  se actualiza mientras siguen cerca, se registra una alerta nueva: cada fila representa una
  observación distinta. Dos trenes parados en la misma estación generan una sola alerta hasta
  que alguno envíe una posición nueva.
- La alerta copia los datos de ambos trenes (no usa claves foráneas a `positions`), porque es
  un hecho histórico que no debe cambiar si se purgan posiciones antiguas.
- Dentro de una misma lectura, un `codComercial` duplicado se descarta en el parser (se
  conserva el primero).

### Tipos de fecha/hora
- Todas las marcas temporales son `TIMESTAMPTZ` (guardadas en UTC internamente): `position_time`
  (el `time` del feed, epoch en segundos), `received_at` y `captured_at` (UTC del colector).
- `hora_llegada_sig_est` llega del feed como hora local de Madrid **sin zona horaria**; se
  interpreta como `Europe/Madrid` y se convierte a UTC antes de guardarla. Es solo informativa.
  Un valor no interpretable se guarda como `NULL`.
- Se evita `TIMESTAMP` sin zona para no mezclar horas locales y UTC en las comparaciones.

### Crecimiento
Con ~160 trenes se insertan del orden de 100-150 posiciones por ciclo (~0,5-0,8 millones al
día). No hay política de retención en esta fase; si el volumen crece conviene purgar o
particionar `positions` por fecha.

## Docker sin Compose (solo el colector, sin BD)
```
docker build -t renfe-collector .
docker run --rm -e ALERT_DISTANCE_METERS=2000 -e POLL_INTERVAL_SECONDS=30 renfe-collector
docker run --rm -e SAMPLE_FILE=sample_flotaLD.json renfe-collector     # sin conexión
```

## Ejecución local y tests
```
pip install -r requirements.txt
python renfe_collector.py
python -m pytest
```
