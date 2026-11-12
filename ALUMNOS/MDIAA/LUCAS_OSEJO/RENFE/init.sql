
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

CREATE TABLE IF NOT EXISTS train_alerts (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id_1 TEXT NOT NULL,
    vehicle_id_2 TEXT NOT NULL,
    latitude_1 DOUBLE PRECISION NOT NULL,
    longitude_1 DOUBLE PRECISION NOT NULL,
    latitude_2 DOUBLE PRECISION NOT NULL,
    longitude_2 DOUBLE PRECISION NOT NULL,
    distance_m DOUBLE PRECISION NOT NULL,
    threshold_m DOUBLE PRECISION NOT NULL,
    captured_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_positions_vehicle_time
    ON train_positions (vehicle_id, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_alerts_time
    ON train_alerts (captured_at DESC);