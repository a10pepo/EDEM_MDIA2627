from datetime import datetime, timezone

import pytest

import renfe_collector as rc

NOW = datetime(2026, 11, 12, 17, 0, tzinfo=timezone.utc)


def train(cod, lat, lon, mat="", ant="A", sig="B"):
    return rc.Train(cod_comercial=cod, lat=lat, lon=lon, time=int(NOW.timestamp()),
                    received_at=NOW, cod_est_ant=ant, cod_est_sig=sig, mat=mat)


def raw(cod="1", lat=40.0, lon=-3.0, **extra):
    d = {"codComercial": cod, "latitud": lat, "longitud": lon, "time": int(NOW.timestamp())}
    d.update(extra)
    return d


def test_haversine_distancia_conocida():
    # 1 grado de latitud = R * pi/180 = 111 194.9 m con R = 6 371 000 m
    assert rc.haversine_m(40.0, -3.0, 41.0, -3.0) == pytest.approx(111_194.9, abs=1)
    assert rc.haversine_m(40.0, -3.0, 40.0, -3.0) == 0


def test_distancia_igual_al_umbral_no_alerta():
    a, b = train("1", 40.0, -3.0), train("2", 40.01, -3.0)
    d = rc.haversine_m(a.lat, a.lon, b.lat, b.lon)
    assert rc.find_alerts([a, b], d, NOW) == []  # estrictamente menor
    assert len(rc.find_alerts([a, b], d + 0.001, NOW)) == 1


def test_mat_compartido_no_alerta():
    a = train("14450", 40.0, -3.0, mat="447009,447010")
    b = train("14461", 40.0, -3.0, mat="447010")
    assert rc.find_alerts([a, b], 5000, NOW) == []


def test_tren_consigo_mismo_no_alerta():
    a = train("1", 40.0, -3.0)
    assert rc.find_alerts([a], 5000, NOW) == []
    assert rc.find_alerts([a, a], 5000, NOW) == []


def test_alerta_solo_en_mismo_tramo():
    a, b = train("1", 40.0, -3.0, mat="1"), train("2", 40.01, -3.0, mat="2")
    (al,) = rc.find_alerts([a, b], 5000, NOW)
    assert al.riesgo_mismo_tramo is True
    assert al.threshold_m == 5000 and al.captured_at == NOW
    # mismo tramo pero lejos del umbral: no alerta
    assert rc.find_alerts([a, train("3", 41.0, -3.0, mat="3")], 5000, NOW) == []


def test_sin_alerta_si_no_coincide_el_tramo():
    a = train("1", 40.0, -3.0, mat="1", ant="A", sig="B")
    cerca = dict(lat=40.0001, lon=-3.0)
    # sentido contrario (A y B invertidos)
    assert rc.find_alerts([a, train("2", **cerca, mat="2", ant="B", sig="A")], 5000, NOW) == []
    # otra estacion siguiente
    assert rc.find_alerts([a, train("3", **cerca, mat="3", ant="A", sig="C")], 5000, NOW) == []
    # los dos en estacion (codEstAnt == codEstSig): sin tramo definido
    e1 = train("4", 40.0, -3.0, mat="4", ant="X", sig="X")
    e2 = train("5", 40.0001, -3.0, mat="5", ant="X", sig="X")
    assert rc.find_alerts([e1, e2], 5000, NOW) == []
    # sin datos de estacion
    assert rc.find_alerts([train("6", 40.0, -3.0, ant=None, sig=None),
                           train("7", 40.0001, -3.0, ant=None, sig=None)], 5000, NOW) == []


@pytest.mark.parametrize("lat,lon", [(91, 0), (-91, 0), (0, 181), (0, -181)])
def test_coordenadas_invalidas(lat, lon):
    trains, warnings = rc.parse_trains({"trenes": [raw(lat=lat, lon=lon)]}, NOW)
    assert trains == []
    assert any(w.startswith("descartado_coordenadas") for w in warnings)


@pytest.mark.parametrize("payload", [{}, None, {"trenes": []}, {"trenes": None}])
def test_respuesta_vacia(payload):
    trains, warnings = rc.parse_trains(payload, NOW)
    assert trains == [] and warnings


def test_campos_obligatorios_duplicados_antiguedad_y_retraso():
    payload = {"trenes": [
        raw("1"),
        raw("1"),                                       # duplicado
        {"latitud": 1, "longitud": 1, "time": 1},       # sin codComercial
        raw("2", time=int(NOW.timestamp()) - 10_000),   # demasiado antiguo
        raw("3", ultRetraso="x"),                       # retraso no convertible
        raw("4", ultRetraso="-380"),
    ]}
    trains, warnings = rc.parse_trains(payload, NOW, max_age_s=300)
    assert [t.cod_comercial for t in trains] == ["1", "3", "4"]
    assert trains[1].ult_retraso is None and trains[2].ult_retraso == -380
    tags = {w.split(":")[0] for w in warnings}
    assert {"descartado_duplicado", "descartado_campos_ausentes",
            "descartado_antiguo", "retraso_invalido"} <= tags


def test_alert_row_orden_canonico_y_tipos():
    a = train("9", 40.0, -3.0, mat="1")
    b = train("2", 40.01, -3.0, mat="2")
    row_ab = rc.alert_row(rc.find_alerts([a, b], 5000, NOW)[0])
    row_ba = rc.alert_row(rc.find_alerts([b, a], 5000, NOW)[0])
    assert row_ab == row_ba            # (A,B) y (B,A) producen la misma fila
    assert row_ab[4] == "2" and row_ab[11] == "9"   # train_a_cod < train_b_cod
    assert row_ab[0].tzinfo is not None             # marcas temporales con zona (UTC)


def test_position_row_hora_madrid_a_utc():
    t = rc.Train("1", 40.0, -3.0, 1794502153, NOW, hora_llegada_sig_est="2026-11-12T19:58:00")
    row = rc.position_row(t)
    assert row[4] == datetime.fromtimestamp(1794502153, tz=timezone.utc)
    assert row[11] == datetime(2026, 11, 12, 18, 58, tzinfo=timezone.utc)  # Madrid = UTC+1 en noviembre
    assert rc.position_row(rc.Train("1", 0, 0, 1, NOW))[11] is None
