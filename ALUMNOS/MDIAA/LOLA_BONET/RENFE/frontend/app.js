/* Frontend de RENFE: consulta la API FastAPI (a través de /api, ver nginx.conf.template)
 * cada POLL_MS milisegundos y pinta posiciones, estelas y alertas. No accede a la base de datos.
 *
 * Flujo: refresh() -> fetchJSON() a /api/getPosiciones, /api/getAlertas y /api/getEstelas -> render*().
 * Estados: "ok" (datos recientes), "sin datos recientes" (la API responde pero el colector no ha
 * guardado posiciones nuevas) y "sin conexión" (la API no responde: se conservan los últimos datos,
 * atenuados, y se avisa).
 */
const POLL_MS = 15000;       // sondeo; la fuente se actualiza cada ~30 s
const TIMEOUT_MS = 8000;     // si la API tarda más, se considera caída
const TRAIL_MIN = 15;        // minutos de estela que se piden y se dibujan
const JUMP_KMH = 350;        // un tramo de estela por encima de esta velocidad es un salto del dato: no se dibuja
const $ = (id) => document.getElementById(id);
const fmt = (n, d = 0) => Number(n).toLocaleString('es-ES', { minimumFractionDigits: d, maximumFractionDigits: d });
const madridTime = (iso) => new Date(iso).toLocaleTimeString('es-ES', { timeZone: 'Europe/Madrid', hour: '2-digit', minute: '2-digit', second: '2-digit' });
const ago = (s) => (s < 90 ? `${Math.round(s)} s` : `${Math.round(s / 60)} min`);

const state = { trenes: null, alertas: null, estelas: {}, lastOk: null, error: null, selected: null, selAlert: null, timer: null };
let estaciones = {};   // id de estación -> nombre (estaciones.json, sacado del GTFS de Renfe)
const sname = (id) => (id ? estaciones[id] || id : '–');

/* ---------- red ---------- */
async function fetchJSON(path) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(path, { signal: ctl.signal, cache: 'no-store' });
    if (!r.ok) throw new Error([502, 503, 504].includes(r.status) ? 'servicio no disponible' : `error ${r.status}`);
    return await r.json();
  } finally { clearTimeout(t); }
}

async function refresh() {
  const limit = $('alert-limit').value;
  try {
    // Posiciones y alertas son imprescindibles: si fallan cuenta como servicio caído.
    // Las estelas son un extra: si fallan solo se dibujan los puntos.
    const [pos, al, est] = await Promise.all([
      fetchJSON('/api/getPosiciones'),
      fetchJSON(`/api/getAlertas?limit=${encodeURIComponent(limit)}`),
      fetchJSON(`/api/getEstelas?minutos=${TRAIL_MIN}`).catch(() => null),
    ]);
    state.trenes = pos; state.alertas = al; state.estelas = est ? est.estelas : {};
    state.lastOk = Date.now(); state.error = null;
  } catch (e) {
    state.error = e.name === 'AbortError' ? 'la API tardó demasiado en responder' : e.message;
  }
  render();
}

function schedule() {
  clearTimeout(state.timer);
  if (!document.hidden) state.timer = setTimeout(async () => { await refresh(); schedule(); }, POLL_MS);
}

/* ---------- estado global ---------- */
function setStatus(kind, text, banner) {
  $('status').className = 'status ' + kind;
  $('status-text').textContent = text;
  const b = $('banner');
  b.hidden = !banner;
  if (banner) { b.className = 'banner ' + (kind === 'err' ? 'err' : 'warn'); b.textContent = banner; }
}

/* Estado y banner. Es barato, así que se llama también cada segundo para refrescar el "hace X s". */
function renderStatus() {
  const secs = state.lastOk ? (Date.now() - state.lastOk) / 1000 : null;
  document.querySelectorAll('.card, .tiles').forEach((e) => e.classList.toggle('stale', !!state.error && !!state.lastOk));
  if (state.error) {
    if (state.lastOk) {
      setStatus('err', `Sin conexión · último dato hace ${ago(secs)}`, `No se puede contactar con el servicio (${state.error}). Se muestran los últimos datos recibidos y se reintentará cada ${POLL_MS / 1000} s.`);
    } else {
      setStatus('err', 'Servicio no disponible', `No se puede contactar con el servicio (${state.error}). Se reintentará cada ${POLL_MS / 1000} s.`);
    }
    return;
  }
  const p = state.trenes;
  if (!p) return;
  if (p.total === 0) {
    const last = p.ultima_recepcion ? `El colector guardó datos por última vez a las ${madridTime(p.ultima_recepcion)} (hora de Madrid).` : 'La base de datos todavía no tiene datos.';
    setStatus('warn', 'Sin datos recientes', `No hay posiciones de menos de ${Math.round(p.max_antiguedad_s / 60)} minutos. ${last} Comprueba que el colector está en marcha.`);
  } else {
    setStatus('ok', `Conectado · actualizado ${secs < 5 ? 'ahora' : 'hace ' + ago(secs)}`, null);
  }
}

/* Pintado completo; solo se llama cuando llegan datos nuevos o el usuario cambia algo. */
function render() {
  renderStatus();
  if (state.error) {
    if (!state.lastOk) renderEmpty('Sin conexión con el servicio.');
    return;                       // con error se conservan los últimos datos en pantalla
  }
  if (!state.trenes) return;
  renderTiles(); renderTrains(); renderAlerts(); renderMap();
}

function renderEmpty(msg) {
  $('tiles').innerHTML = '';
  $('trains').tBodies[0].innerHTML = `<tr><td class="empty" colspan="7">${msg}</td></tr>`;
  $('alerts').tBodies[0].innerHTML = `<tr><td class="empty" colspan="4">${msg}</td></tr>`;
  $('map').innerHTML = '';
}

/* ---------- utilidades de DOM ---------- */
// Se construye el DOM con textContent (nunca innerHTML con datos de la API) para evitar inyección de HTML.
function cell(tr, text, cls) { const td = document.createElement('td'); td.textContent = text; if (cls) td.className = cls; tr.appendChild(td); return td; }
function el(tag, text, cls) { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (cls) e.className = cls; return e; }
const alertedTrains = () => new Set((state.alertas || []).flatMap((x) => [x.tren_a.cod_comercial, x.tren_b.cod_comercial]));

/* ---------- resumen ---------- */
function renderTiles() {
  const p = state.trenes, a = state.alertas;
  const tiles = [
    [fmt(p.total), 'trenes con posición reciente'],
    [fmt(a.length), 'alertas mostradas'],
    [a.length ? fmt(a[0].threshold_m) + ' m' : '–', 'umbral de la última alerta'],
    [a.length ? madridTime(a[0].captured_at) : '–', 'hora de la última alerta (Madrid)'],
  ];
  $('tiles').replaceChildren(...tiles.map(([n, l]) => { const d = el('div', undefined, 'tile'); d.append(el('b', n), el('span', l)); return d; }));
}

/* ---------- tabla de trenes ---------- */
function renderTrains() {
  const q = $('filter').value.trim().toLowerCase();
  const hot = alertedTrains();
  const rows = state.trenes.trenes.filter((t) => !q || t.cod_comercial.includes(q) || t.mat.toLowerCase().includes(q));
  const tb = $('trains').tBodies[0];
  tb.replaceChildren();
  if (!rows.length) {
    const tr = tb.insertRow(); cell(tr, state.trenes.total ? 'Ningún tren coincide con el filtro.' : 'No hay posiciones recientes.', 'empty').colSpan = 7; return;
  }
  const sel = selectedTrains();
  rows.forEach((t) => {
    const tr = tb.insertRow(); tr.dataset.c = t.cod_comercial;
    if (hot.has(t.cod_comercial)) tr.classList.add('alerted');
    if (sel.has(t.cod_comercial)) tr.classList.add('sel');
    cell(tr, t.cod_comercial); cell(tr, t.mat || '–');
    cell(tr, t.lat.toFixed(5), 'n'); cell(tr, t.lon.toFixed(5), 'n');
    cell(tr, t.cod_est_ant === t.cod_est_sig ? `En ${sname(t.cod_est_ant)}` : `${sname(t.cod_est_ant)} → ${sname(t.cod_est_sig)}`).title = `${t.cod_est_ant || '–'} → ${t.cod_est_sig || '–'}`;
    cell(tr, t.ult_retraso === null ? '–' : `${t.ult_retraso} min`, 'n');
    cell(tr, ago(t.edad_posicion_s), 'n');
  });
}

/* ---------- tabla de alertas: entre qué trenes y por qué ---------- */
const tramo = (t) => (t.cod_est_ant === t.cod_est_sig ? `en ${sname(t.cod_est_ant)}` : `${sname(t.cod_est_ant)} → ${sname(t.cod_est_sig)}`);

function whyCell(a) {
  const td = el('td', undefined, 'why'), ul = el('ul');
  const A = a.tren_a, B = a.tren_b;
  const dist = `Distancia ${fmt(a.distance_m)} m, menor que el umbral de ${fmt(a.threshold_m)} m`;
  if (a.riesgo_mismo_tramo) {
    // Regla actual: mismo tramo A->B + distancia < umbral + unidades distintas
    ul.append(el('li', `Los dos van en el mismo tramo: ${tramo(A)}`));
    ul.append(el('li', dist));
    ul.append(el('li', `Son unidades distintas (matrícula ${A.mat || '–'} y ${B.mat || '–'})`));
  } else {
    // Alertas guardadas con la regla anterior, que solo miraba la distancia
    ul.append(el('li', dist));
    ul.append(el('li', `Tramos distintos: el ${A.cod_comercial} ${tramo(A)} y el ${B.cod_comercial} ${tramo(B)}`));
    ul.append(el('li', 'Alerta de la regla anterior (solo por distancia)', 'old'));
  }
  td.appendChild(ul); return td;
}

function renderAlerts() {
  const tb = $('alerts').tBodies[0];
  tb.replaceChildren();
  if (!state.alertas.length) {
    const tr = tb.insertRow(); cell(tr, 'No hay alertas registradas.', 'empty').colSpan = 4; return;
  }
  state.alertas.forEach((a) => {
    const tr = tb.insertRow(); tr.dataset.alert = a.id;
    if (state.selAlert === a.id) tr.classList.add('sel-al');
    cell(tr, madridTime(a.captured_at));
    const pair = cell(tr, '', 'wrap');
    [['A', a.tren_a], ['B', a.tren_b]].forEach(([, t], i) => {
      if (i) pair.append(' ↔ ');
      pair.append(el('b', `Tren ${t.cod_comercial}`));
    });
    pair.append(el('div', `mat ${a.tren_a.mat || '–'} · mat ${a.tren_b.mat || '–'}`, 'small'));
    const d = cell(tr, `${fmt(a.distance_m)} m`, 'n'); d.append(el('div', `umbral ${fmt(a.threshold_m)} m`, 'small'));
    tr.appendChild(whyCell(a));
  });
}

/* ---------- mapa: último dato de cada tren + estela ---------- */
// Proyección equirrectangular fija sobre España peninsular (estable entre actualizaciones).
const W = 900, K = Math.cos(40 * Math.PI / 180), LON0 = -9.6, LON1 = 4.6, LAT0 = 35.8, LAT1 = 43.9;
const SC = (W - 20) / ((LON1 - LON0) * K), H = Math.round((LAT1 - LAT0) * SC + 20);
const px = (lon) => (lon - LON0) * K * SC + 10, py = (lat) => (LAT1 - lat) * SC + 10;
let vb = { x: 0, y: 0, w: W, h: H };       // zona visible (zoom/arrastre); persiste entre actualizaciones
const NS = 'http://www.w3.org/2000/svg';
const svgEl = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };

function hav(a, b, c, d) {
  const R = 6371000, r = Math.PI / 180, dp = (c - a) * r, dl = (d - b) * r;
  const x = Math.sin(dp / 2) ** 2 + Math.cos(a * r) * Math.cos(c * r) * Math.sin(dl / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(x));
}

/* Parte la estela en tramos continuos: si dos muestras seguidas implican más de JUMP_KMH,
 * es un salto del dato (no un movimiento real) y no se unen con una línea. */
function trailSegments(points) {
  const segs = []; let cur = [];
  points.forEach((p, i) => {
    if (i) {
      const q = points[i - 1], dt = p[2] - q[2];
      const kmh = dt > 0 ? hav(q[0], q[1], p[0], p[1]) / dt * 3.6 : 0;
      if (kmh > JUMP_KMH) { segs.push(cur); cur = []; }
    }
    cur.push(p);
  });
  segs.push(cur);
  return segs.filter((s) => s.length > 1);
}

function selectedTrains() {
  const s = new Set();
  if (state.selected) s.add(state.selected);
  const a = (state.alertas || []).find((x) => x.id === state.selAlert);
  if (a) { s.add(a.tren_a.cod_comercial); s.add(a.tren_b.cod_comercial); }
  return s;
}

function renderMap() {
  const svg = $('map'), ts = state.trenes ? state.trenes.trenes : [];
  svg.replaceChildren();
  svg.setAttribute('viewBox', `${vb.x} ${vb.y} ${vb.w} ${vb.h}`);
  if (!ts.length) return;
  const k = vb.w / W;                       // al acercar, los puntos conservan su tamaño en pantalla
  const hot = alertedTrains(), sel = selectedTrains();
  const gTrail = svgEl('g', {}, svg), gAlert = svgEl('g', {}, svg), gDot = svgEl('g', {}, svg);

  // 1) estelas (las seleccionadas, más gruesas y opacas)
  ts.forEach((t) => {
    const pts = state.estelas[t.cod_comercial];
    if (!pts || pts.length < 2) return;
    const on = sel.has(t.cod_comercial), isHot = hot.has(t.cod_comercial);
    trailSegments(pts).forEach((seg) => svgEl('polyline', {
      points: seg.map((p) => `${px(p[1]).toFixed(1)},${py(p[0]).toFixed(1)}`).join(' '), fill: 'none',
      stroke: isHot ? 'var(--alert)' : 'var(--accent)', 'stroke-width': on ? 2.6 : 1.3,
      'stroke-opacity': on ? 0.95 : 0.4, 'vector-effect': 'non-scaling-stroke', 'stroke-linejoin': 'round',
    }, gTrail));
  });

  // 2) alerta seleccionada: línea entre los dos trenes
  const al = (state.alertas || []).find((x) => x.id === state.selAlert);
  if (al) {
    const A = ts.find((t) => t.cod_comercial === al.tren_a.cod_comercial), B = ts.find((t) => t.cod_comercial === al.tren_b.cod_comercial);
    const a = A ? [A.lat, A.lon] : [al.tren_a.lat, al.tren_a.lon], b = B ? [B.lat, B.lon] : [al.tren_b.lat, al.tren_b.lon];
    svgEl('line', { x1: px(a[1]), y1: py(a[0]), x2: px(b[1]), y2: py(b[0]), stroke: 'var(--alert)', 'stroke-width': 2, 'stroke-dasharray': '5 4', 'vector-effect': 'non-scaling-stroke' }, gAlert);
  }

  // 3) último dato de cada tren (los de alerta y los seleccionados encima)
  const order = [...ts.filter((t) => !hot.has(t.cod_comercial)), ...ts.filter((t) => hot.has(t.cod_comercial) && !sel.has(t.cod_comercial)), ...ts.filter((t) => sel.has(t.cod_comercial))];
  order.forEach((t) => {
    const isHot = hot.has(t.cod_comercial), isSel = sel.has(t.cod_comercial);
    const c = svgEl('circle', {
      cx: px(t.lon), cy: py(t.lat), r: (isSel ? 6.5 : isHot ? 4.8 : 3.4) * k,
      fill: isHot ? 'var(--alert)' : 'var(--accent)', stroke: isSel ? 'var(--ink)' : 'var(--card)',
      'stroke-width': isSel ? 2 : 1, 'vector-effect': 'non-scaling-stroke', 'data-c': t.cod_comercial,
    }, gDot);
    c.style.cursor = 'pointer';
    const title = document.createElementNS(NS, 'title');
    title.textContent = `Tren ${t.cod_comercial} · ${t.lat.toFixed(4)}, ${t.lon.toFixed(4)} · hace ${ago(t.edad_posicion_s)} · ${tramo(t)}`;
    c.appendChild(title);
  });
}

/* ---------- zoom y arrastre del mapa ---------- */
const svgMap = $('map');
let raf = 0, drag = null;
const redraw = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(renderMap); };
svgMap.addEventListener('wheel', (e) => {
  e.preventDefault();
  const r = svgMap.getBoundingClientRect(), fx = (e.clientX - r.left) / r.width, fy = (e.clientY - r.top) / r.height;
  const f = e.deltaY < 0 ? 0.8 : 1.25, nw = Math.min(W, Math.max(W / 40, vb.w * f)), nh = nw * H / W;
  vb = { x: vb.x + (vb.w - nw) * fx, y: vb.y + (vb.h - nh) * fy, w: nw, h: nh };
  vb.x = Math.min(Math.max(0, vb.x), W - vb.w); vb.y = Math.min(Math.max(0, vb.y), H - vb.h);
  redraw();
}, { passive: false });
svgMap.addEventListener('pointerdown', (e) => { drag = { x: e.clientX, y: e.clientY, vb: { ...vb }, moved: false }; });
window.addEventListener('pointermove', (e) => {
  if (!drag) return;
  if (Math.abs(e.clientX - drag.x) + Math.abs(e.clientY - drag.y) > 4) { drag.moved = true; svgMap.classList.add('drag'); }
  if (!drag.moved) return;
  const r = svgMap.getBoundingClientRect();
  vb.x = Math.min(Math.max(0, drag.vb.x - (e.clientX - drag.x) / r.width * vb.w), W - vb.w);
  vb.y = Math.min(Math.max(0, drag.vb.y - (e.clientY - drag.y) / r.height * vb.h), H - vb.h);
  redraw();
});
window.addEventListener('pointerup', () => { svgMap.classList.remove('drag'); setTimeout(() => { drag = null; }, 0); });
$('reset-zoom').addEventListener('click', () => { vb = { x: 0, y: 0, w: W, h: H }; renderMap(); });

/* ---------- selección ---------- */
function repaintSelection() { if (state.trenes) { renderTrains(); renderAlerts(); renderMap(); } }
svgMap.addEventListener('click', (e) => {
  if (drag && drag.moved) return;                       // era un arrastre, no un clic
  const c = e.target.closest('[data-c]');
  state.selAlert = null;
  state.selected = c && state.selected !== c.dataset.c ? c.dataset.c : null;
  repaintSelection();
});
$('trains').addEventListener('click', (e) => {
  const tr = e.target.closest('[data-c]'); if (!tr) return;
  state.selAlert = null; state.selected = state.selected === tr.dataset.c ? null : tr.dataset.c;
  repaintSelection();
});
$('alerts').addEventListener('click', (e) => {
  const tr = e.target.closest('[data-alert]'); if (!tr) return;
  const id = Number(tr.dataset.alert);
  state.selected = null; state.selAlert = state.selAlert === id ? null : id;
  repaintSelection();
});
$('filter').addEventListener('input', () => state.trenes && renderTrains());
$('alert-limit').addEventListener('change', async () => { await refresh(); schedule(); });
document.addEventListener('visibilitychange', () => { if (!document.hidden) { refresh().then(schedule); } else clearTimeout(state.timer); });
setInterval(() => { if (state.lastOk) renderStatus(); }, 1000);   // refresca el "hace X s" sin llamar a la API

/* ---------- arranque ---------- */
$('poll-s').textContent = POLL_MS / 1000;
$('trail-min').textContent = TRAIL_MIN;
fetch('estaciones.json').then((r) => r.json()).catch(() => ({}))   // sin nombres se muestran los códigos
  .then((e) => { estaciones = e; return refresh(); }).then(schedule);
