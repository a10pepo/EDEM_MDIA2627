--Tabla para las posiciones de los trenes:
CREATE TABLE IF NOT EXISTS train_positions (
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


-- Tabla para las alertas de proximidad
CREATE TABLE IF NOT EXISTS train_alerts (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id_1 TEXT NOT NULL,
    vehicle_id_2 TEXT NOT NULL,
    distance_meters DOUBLE PRECISION NOT NULL,
    lat_1 DOUBLE PRECISION NOT NULL,
    lon_1 DOUBLE PRECISION NOT NULL,
    lat_2 DOUBLE PRECISION NOT NULL,
    lon_2 DOUBLE PRECISION NOT NULL,
    alerted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices recomendados para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_train_positions_vehicle_time ON train_positions (vehicle_id, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_train_alerts_date ON train_alerts (alerted_at DESC);