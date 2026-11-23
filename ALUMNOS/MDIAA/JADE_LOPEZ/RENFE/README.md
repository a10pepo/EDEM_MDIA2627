# Monitorización de Trenes RENFE en Tiempo Real

Sistema End-to-End (E2E) para la ingesta, almacenamiento, detección de proximidad y visualización en tiempo real de las posiciones de los trenes de Larga Distancia de RENFE a partir de sus datos abiertos GTFS-RT.

---

## Arquitectura del Proyecto

El sistema está compuesto por cuatro capas desacopladas y orquestadas mediante Docker Compose:

1. **Recolector (`renfe_collector.py`):** Consulta periódicamente el feed público de posiciones de RENFE (`vehicle_positions_LD.json`), normaliza las marcas temporales, calcula las distancias geográficas entre trenes mediante la fórmula de Haversine y persiste tanto las posiciones como las alertas de proximidad.
2. **Base de Datos (`PostgreSQL 16`):** Almacena el histórico de posiciones (`train_positions`) y las alertas detectadas (`proximity_alerts`) con persistencia en volumen Docker e inicialización automática mediante `init.sql`.
3. **Backend API (`api.py` - FastAPI):** Expone endpoints REST para consultar la última posición conocida de cada tren, su histórico reciente y las alertas de proximidad filtrables por distancia.
4. **Frontend (`frontend/index.html`):** Interfaz web estática que consume la API cada 10 segundos y representa los trenes activos sobre un mapa topográfico (Leaflet + Esri) junto con el panel de alertas en vivo.

---

## Estructura del Repositorio

```text
RENFE/
├── frontend/
│   └── index.html          # Panel de visualización web (mapa y tablas en tiempo real)
├── .env.example            # Plantilla de variables de entorno
├── .gitignore              # Exclusión de credenciales y archivos temporales
├── api.py                  # API REST con FastAPI y documentación Swagger
├── docker-compose.yml      # Orquestación de servicios (db, collector, backend)
├── Dockerfile              # Imagen Python para el recolector y el backend
├── init.sql                # Esquema inicial de tablas e índices en PostgreSQL
├── README.md               # Documentación del proyecto
├── renfe_collector.py      # Script de ingesta y cálculo de proximidad (Haversine)
└── requirements.txt        # Dependencias de Python