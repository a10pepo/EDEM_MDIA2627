-- Esquema PostgreSQL del colector RENFE. Idempotente: el colector lo ejecuta al conectar.

-- Una fila por posicion GPS de un tren. El feed repite la misma posicion (mismo `time`)
-- en lecturas consecutivas, asi que la clave natural (tren, hora de la posicion) evita duplicados.
CREATE TABLE IF NOT EXISTS positions (
    id                   BIGSERIAL PRIMARY KEY,
    cod_comercial        TEXT             NOT NULL,
    mat                  TEXT             NOT NULL DEFAULT '',
    lat                  DOUBLE PRECISION NOT NULL CHECK (lat BETWEEN -90 AND 90),
    lon                  DOUBLE PRECISION NOT NULL CHECK (lon BETWEEN -180 AND 180),
    position_time        TIMESTAMPTZ      NOT NULL,   -- `time` del feed (epoch -> UTC)
    received_at          TIMESTAMPTZ      NOT NULL,   -- recepcion por el colector (UTC)
    cod_est_ant          TEXT,
    cod_est_sig          TEXT,
    cod_origen           TEXT,
    cod_destino          TEXT,
    ult_retraso          INTEGER,                     -- minutos; NULL si no era un entero
    hora_llegada_sig_est TIMESTAMPTZ,                 -- hora local de Madrid convertida; solo informativa
    extra                JSONB            NOT NULL DEFAULT '{}',  -- codProduct, p, accesible tal cual
    CONSTRAINT positions_tren_hora_uq UNIQUE (cod_comercial, position_time)
);
-- Posiciones recientes por vehiculo: WHERE cod_comercial = ? ORDER BY position_time DESC LIMIT n
CREATE INDEX IF NOT EXISTS positions_vehiculo_reciente_idx
    ON positions (cod_comercial, position_time DESC);
-- Ultimas posiciones de toda la flota (mapa)
CREATE INDEX IF NOT EXISTS positions_received_idx ON positions (received_at DESC);

-- Una fila por alerta. Los datos de ambos trenes se copian en la fila (la alerta es un
-- hecho historico y no debe cambiar aunque se purguen posiciones). El par se guarda en
-- orden canonico (train_a_cod < train_b_cod) para que (A,B) y (B,A) sean la misma alerta.
CREATE TABLE IF NOT EXISTS alerts (
    id                    BIGSERIAL PRIMARY KEY,
    captured_at           TIMESTAMPTZ      NOT NULL,   -- momento de la lectura (UTC)
    distance_m            DOUBLE PRECISION NOT NULL CHECK (distance_m >= 0),
    threshold_m           DOUBLE PRECISION NOT NULL CHECK (threshold_m > 0),
    riesgo_mismo_tramo    BOOLEAN          NOT NULL,

    train_a_cod           TEXT             NOT NULL,
    train_a_mat           TEXT             NOT NULL DEFAULT '',
    train_a_lat           DOUBLE PRECISION NOT NULL,
    train_a_lon           DOUBLE PRECISION NOT NULL,
    train_a_est_ant       TEXT,
    train_a_est_sig       TEXT,
    train_a_position_time TIMESTAMPTZ      NOT NULL,

    train_b_cod           TEXT             NOT NULL,
    train_b_mat           TEXT             NOT NULL DEFAULT '',
    train_b_lat           DOUBLE PRECISION NOT NULL,
    train_b_lon           DOUBLE PRECISION NOT NULL,
    train_b_est_ant       TEXT,
    train_b_est_sig       TEXT,
    train_b_position_time TIMESTAMPTZ      NOT NULL,

    CONSTRAINT alerts_orden_par_ck CHECK (train_a_cod < train_b_cod),
    -- misma pareja con las mismas dos posiciones = misma alerta (no se repite en cada lectura)
    CONSTRAINT alerts_par_posiciones_uq UNIQUE
        (train_a_cod, train_b_cod, train_a_position_time, train_b_position_time)
);
-- Alertas por fecha
CREATE INDEX IF NOT EXISTS alerts_captured_idx ON alerts (captured_at DESC);
-- Historial de alertas de un tren concreto
CREATE INDEX IF NOT EXISTS alerts_train_a_idx ON alerts (train_a_cod, captured_at DESC);
CREATE INDEX IF NOT EXISTS alerts_train_b_idx ON alerts (train_b_cod, captured_at DESC);
-- Historial reciente de toda la flota (estelas): WHERE position_time > now() - intervalo
CREATE INDEX IF NOT EXISTS positions_position_time_idx ON positions (position_time DESC);
