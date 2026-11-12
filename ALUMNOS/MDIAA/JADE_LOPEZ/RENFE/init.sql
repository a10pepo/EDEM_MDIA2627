--Crear la tabla posiciones
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

CREATE INDEX IF NOT EXISTS idx_positions_vehicle_time ON train_positions (vehicle_id, received_at DESC);

--Crear la tabla alertas
CREATE TABLE IF NOT EXISTS proximity_alerts (
    id BIGSERIAL PRIMARY KEY,
    train_1_id TEXT NOT NULL,
    train_2_id TEXT NOT NULL,
    train_1_lat DOUBLE PRECISION NOT NULL,
    train_1_lon DOUBLE PRECISION NOT NULL,
    train_2_lat DOUBLE PRECISION NOT NULL,
    train_2_lon DOUBLE PRECISION NOT NULL,
    distance_meters DOUBLE PRECISION NOT NULL,
    threshold_meters DOUBLE PRECISION NOT NULL,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alerts_detected_at ON proximity_alerts (detected_at DESC);