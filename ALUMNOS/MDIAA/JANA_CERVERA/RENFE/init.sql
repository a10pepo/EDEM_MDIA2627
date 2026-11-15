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

CREATE TABLE IF NOT EXISTS proximity_alerts (
    id BIGSERIAL PRIMARY KEY,
    vehicle_1_id TEXT NOT NULL,
    vehicle_2_id TEXT NOT NULL,
    lat_1 DOUBLE PRECISION NOT NULL,
    lon_1 DOUBLE PRECISION NOT NULL,
    lat_2 DOUBLE PRECISION NOT NULL,
    lon_2 DOUBLE PRECISION NOT NULL,
    distance_meters DOUBLE PRECISION NOT NULL,
    threshold_meters DOUBLE PRECISION NOT NULL DEFAULT 500,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices para consultas rápidas
CREATE INDEX idx_positions_vehicle_time ON train_positions (vehicle_id, received_at DESC);
CREATE INDEX idx_alerts_captured_at ON proximity_alerts (captured_at DESC);