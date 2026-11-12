-- Fechas: TIMESTAMPTZ (siempre UTC en origen). Deduplicación: una posición se
-- identifica por (vehicle_id, position_timestamp); si la fuente repite la lectura se ignora.
CREATE TABLE IF NOT EXISTS train_positions (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id TEXT NOT NULL,
    trip_id TEXT,
    route_id TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    position_timestamp TIMESTAMPTZ,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    raw_payload JSONB,
    UNIQUE (vehicle_id, position_timestamp)
);
CREATE INDEX IF NOT EXISTS idx_positions_vehicle_recent
    ON train_positions (vehicle_id, received_at DESC);

CREATE TABLE IF NOT EXISTS proximity_alerts (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id_a TEXT NOT NULL,
    vehicle_id_b TEXT NOT NULL,
    lat_a DOUBLE PRECISION NOT NULL,
    lon_a DOUBLE PRECISION NOT NULL,
    lat_b DOUBLE PRECISION NOT NULL,
    lon_b DOUBLE PRECISION NOT NULL,
    distance_m DOUBLE PRECISION NOT NULL,
    threshold_m DOUBLE PRECISION NOT NULL,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_alerts_captured_at ON proximity_alerts (captured_at DESC);
