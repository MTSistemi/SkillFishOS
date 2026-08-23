// I pezzi della telemetria che servono a due pagine: la dashboard e la
// telemetria a schermo intero. Stavano dentro app.js, e per la pagina nuova la
// strada corta sarebbe stata copiarli: due copie dello stesso grafico che
// divergono al primo ritocco.
//
// ⚠️ Qui NON si definisce `$`: app.js lo dichiara con `const`, e una seconda
// dichiarazione nello stesso ambito globale rompe la pagina prima che parta.
// Chi carica questo file deve avere gia' il suo.
// ⚠️ Va caricato PRIMA di app.js, che usa TELEM.

// ---------------- charts ----------------
// Round the axis to human numbers (0/1000/2000, not -160/1394/2948). Two rules
// beyond plain rounding: zero becomes the floor when the data sits near it (a MHz
// or RPM chart must never show a negative baseline), and the step comes from the
// *unpadded* range, or the padding inflates it and 3992 MHz lands on a 0-6000 axis.
function niceStep(raw) {
  if (!(raw > 0)) return 1;
  const mag = Math.pow(10, Math.floor(Math.log10(raw))), n = raw / mag;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * mag;
}

function niceScale(lo, hi, ticks) {
  // a dead-flat series must not get a wildly zoomed axis: 800/800 MHz would
  // otherwise be drawn on a 799.8-801.2 scale, amplifying nothing into noise
  if (hi - lo < Math.max(1e-9, Math.abs(hi) * 0.005)) {
    if (hi === 0) { lo = 0; hi = 1; }
    else { const band = Math.abs(hi) * 0.05; lo = hi - band; hi = hi + band; }
  }
  const nonneg = lo >= 0;
  if (nonneg && lo < hi - lo) lo = 0;
  const span = hi - lo, step = niceStep(span / Math.max(1, ticks)), pad = span * 0.06;
  let nlo = (nonneg && lo === 0) ? 0 : Math.floor((lo - pad) / step) * step;
  if (nonneg) nlo = Math.max(0, nlo);
  return { lo: nlo, hi: Math.ceil((hi + pad) / step) * step, step };
}

class Mini {
  constructor(canvas, series) { this.c = canvas; this.series = series; this.data = series.map(() => []); this.max = 90; }
  push(vals) { vals.forEach((v, i) => { const d = this.data[i]; d.push(v == null ? (d.length ? d[d.length - 1] : 0) : v); if (d.length > this.max) d.shift(); }); this.draw(); }
  draw() {
    const cv = this.c, dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
    if (cv.width !== w * dpr) { cv.width = w * dpr; cv.height = h * dpr; }
    const x = cv.getContext("2d"); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
    let all = []; this.data.forEach(d => all = all.concat(d)); if (!all.length) return;
    const sc = niceScale(Math.min(...all), Math.max(...all), 4);   // padding included
    let lo = sc.lo, hi = sc.hi;
    // plot area: a left gutter carries the y-axis values, otherwise the scale is unreadable
    const gx = 40, gw = Math.max(4, w - gx - 3), gy = 7, gh = Math.max(4, h - 14), span = hi - lo;
    let dec = 0;   // exactly the decimals the step needs: 0.25 -> "0.25", never "0.2"
    while (dec < 3 && Math.abs(+sc.step.toFixed(dec) - sc.step) > 1e-9) dec++;
    x.font = "10px 'DejaVu Sans Mono',monospace"; x.textAlign = "right"; x.textBaseline = "middle";
    x.lineWidth = 1;
    for (let v = lo; v <= hi + sc.step / 2; v += sc.step) {
      const yy = Math.round(gy + gh - gh * (v - lo) / span) + 0.5;
      x.strokeStyle = "rgba(216,168,73,.10)"; x.beginPath(); x.moveTo(gx, yy); x.lineTo(gx + gw, yy); x.stroke();
      x.fillStyle = "rgba(185,160,122,.8)"; x.fillText(v.toFixed(dec), gx - 6, yy);
    }
    this.data.forEach((d, i) => { if (d.length < 2) return; x.beginPath(); d.forEach((v, j) => { const px = gx + gw * j / (d.length - 1), py = gy + gh - gh * (v - lo) / span; j ? x.lineTo(px, py) : x.moveTo(px, py); }); x.strokeStyle = this.series[i].c; x.lineWidth = 1.6; x.lineJoin = "round"; x.stroke(); });
  }
}

// Per core/thread frequency bars. `threads` is [[cpu, core, mhz|null], ...] straight
// off the telemetry stream; a null MHz means the Tuner has that thread parked.
function coreColor(t) {
  const a = t < 0.5 ? [0x6b, 0x5a, 0x34] : [0xd8, 0xa8, 0x49],
        b = t < 0.5 ? [0xd8, 0xa8, 0x49] : [0xe0, 0x6b, 0x39],
        k = t < 0.5 ? t / 0.5 : (t - 0.5) / 0.5;
  return "rgb(" + a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(",") + ")";
}

function renderCores(root, threads) {
  if (!Array.isArray(threads) || !threads.length) return;
  const bars = $(".cbars", root), axis = $(".cat", root), stat = $(".cstat", root);
  const live = threads.filter(t => t[2] != null).map(t => t[2]);
  let hi = Math.max(1000, live.length ? Math.max(...live) : 0);
  hi = Math.ceil(hi / 500) * 500;                       // round, stable scale
  if (root._n !== threads.length) {                     // rebuild only on hotplug
    root._n = threads.length;
    bars.innerHTML = threads.map(t =>
      `<div class="cbar"><span class="v"></span><span class="t"><i class="b"></i></span><span class="n">${t[1]}·${t[0]}</span></div>`).join("");
  }
  if (root._hi !== hi) {
    root._hi = hi;
    axis.innerHTML = [0, 1, 2, 3, 4].map(i =>
      `<span style="top:${i * 25}%">${Math.round(hi - hi * i / 4)}</span>`).join("");
  }
  const els = bars.children;
  threads.forEach((t, i) => {
    const el = els[i]; if (!el) return;
    const mhz = t[2], b = $(".b", el);
    el.classList.toggle("off", mhz == null);
    if (mhz == null) { $(".v", el).textContent = T("c_off"); b.style.background = ""; return; }
    const k = Math.max(0, Math.min(1, mhz / hi));
    $(".v", el).textContent = Math.round(mhz);
    b.style.height = (k * 100).toFixed(1) + "%";
    b.style.background = "linear-gradient(180deg," + coreColor(k) + " 0%, rgba(0,0,0,0) 260%)";
    b.style.borderTop = "1px solid " + coreColor(k);
  });
  if (stat) stat.innerHTML = live.length
    ? `min <b>${Math.round(Math.min(...live))}</b> · ${T("c_avg")} <b>${Math.round(live.reduce((a, v) => a + v, 0) / live.length)}</b> · max <b>${Math.round(Math.max(...live))}</b> · ${T("c_online")} <b>${live.length}/${threads.length}</b>`
    : "";
}

const TELEM = [
  { t: "t_temp", u: "°C", s: [{ k: "cpu_temp", l: "CPU", c: "#e8c878" }, { k: "gpu_temp", l: "GPU", c: "#e07b39" }] },
  { t: "t_load", u: "%", s: [{ k: "cpu_load", l: "CPU", c: "#5fd24f" }, { k: "gpu_util", l: "GPU", c: "#49b6e0" }] },
  { t: "t_freq", u: "MHz", s: [{ k: "cpu_mhz", l: "CPU", c: "#9bd24f" }, { k: "gpu_freq", l: "GPU", c: "#49b6e0" }] },
  { t: "t_pow", u: "W", s: [{ k: "gpu_power", l: "GPU", c: "#e0d24f" }] },
  { t: "t_volt", u: "mV", s: [{ k: "gpu_mv", l: "GPU", c: "#c98be0" }, { k: "cpu_mv", l: "CPU", c: "#e8a878" }] },
  { t: "t_fan", u: "RPM", s: [{ k: "fan", l: "FAN", c: "#d8a849" }] },
];
