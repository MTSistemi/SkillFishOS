"use strict";
// SkillFish Remote - dynamic, module-composed dashboard frontend.
const $ = (s, r = document) => r.querySelector(s);
const api = (p, opt) => fetch(p, Object.assign({ credentials: "same-origin" }, opt));
const post = (p, body) => api(p, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });
function toast(msg, ok = true) {
  let t = $("#toast");
  if (!t) { t = document.createElement("div"); t.id = "toast"; document.body.appendChild(t); }
  t.textContent = msg; t.style.cssText =
    "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:99;padding:10px 18px;border-radius:10px;" +
    "font-weight:600;font-size:.9rem;color:#1a130a;background:" + (ok ? "#d8a849" : "#e07b5a") +
    ";box-shadow:0 8px 24px rgba(0,0,0,.5);opacity:1;transition:opacity .4s";
  clearTimeout(toast._t); toast._t = setTimeout(() => { t.style.opacity = "0"; }, 2200);
}
async function action(p, body, okmsg) {
  try { const j = await (await post(p, body)).json(); toast(j.ok === false ? (j.error || "errore") : (okmsg || "fatto"), j.ok !== false); return j; }
  catch (e) { toast("errore di rete", false); }
}

// ---- canvas sparkline chart (multi-series, rolling) ----
class Mini {
  constructor(canvas, series, unit) {
    this.c = canvas; this.series = series; this.unit = unit;
    this.data = series.map(() => []); this.max = 90;
  }
  push(vals) {
    vals.forEach((v, i) => {
      const d = this.data[i];
      d.push(v == null ? (d.length ? d[d.length - 1] : 0) : v);
      if (d.length > this.max) d.shift();
    });
    this.draw();
  }
  draw() {
    const cv = this.c, dpr = window.devicePixelRatio || 1;
    const w = cv.clientWidth, h = cv.clientHeight;
    if (cv.width !== w * dpr) { cv.width = w * dpr; cv.height = h * dpr; }
    const x = cv.getContext("2d"); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
    let all = []; this.data.forEach(d => all = all.concat(d));
    if (!all.length) return;
    let lo = Math.min(...all), hi = Math.max(...all);
    if (hi - lo < 1e-6) hi = lo + 1; const m = (hi - lo) * 0.15; lo -= m; hi += m;
    this.data.forEach((d, i) => {
      if (d.length < 2) return;
      const col = this.series[i].c;
      x.beginPath();
      d.forEach((v, j) => {
        const px = w * j / (d.length - 1), py = h - h * (v - lo) / (hi - lo);
        j ? x.lineTo(px, py) : x.moveTo(px, py);
      });
      x.strokeStyle = col; x.lineWidth = 1.6; x.lineJoin = "round"; x.stroke();
    });
  }
  cur(i) { const d = this.data[i]; return d.length ? d[d.length - 1] : null; }
}

const TELEM = [
  { t: "Temperatura", u: "°C", s: [{ k: "cpu_temp", l: "CPU", c: "#e8c878" }, { k: "gpu_temp", l: "GPU", c: "#e07b39" }] },
  { t: "Carico", u: "%", s: [{ k: "cpu_load", l: "CPU", c: "#5fd24f" }, { k: "gpu_util", l: "GPU", c: "#49b6e0" }] },
  { t: "Frequenza", u: "MHz", s: [{ k: "cpu_mhz", l: "CPU", c: "#9bd24f" }, { k: "gpu_freq", l: "GPU", c: "#49b6e0" }] },
  { t: "Potenza", u: "W", s: [{ k: "gpu_power", l: "GPU", c: "#e0d24f" }] },
  { t: "Voltaggio", u: "mV", s: [{ k: "gpu_mv", l: "GPU", c: "#c98be0" }, { k: "cpu_mv", l: "CPU", c: "#e8a878" }] },
  { t: "Ventola", u: "RPM", s: [{ k: "fan", l: "FAN", c: "#d8a849" }] },
];

const RENDER = {
  telemetry(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>📊 Telemetria <span class="pill" id="tlive">live</span></h3><div class="charts"></div>';
    const box = $(".charts", card); const charts = [];
    TELEM.forEach(spec => {
      const el = document.createElement("div"); el.className = "chart";
      const labs = spec.s.map(s => `<span style="color:${s.c}">${s.l} <b class="val" data-k="${s.k}">–</b></span>`).join(" ");
      el.innerHTML = `<div class="lab"><span>${spec.t} (${spec.u})</span><span>${labs}</span></div><canvas></canvas>`;
      box.appendChild(el);
      charts.push({ spec, m: new Mini($("canvas", el), spec.s, spec.u), el });
    });
    const es = new EventSource("/api/telemetry");
    es.onmessage = ev => {
      let v; try { v = JSON.parse(ev.data); } catch (e) { return; }
      charts.forEach(c => {
        c.m.push(c.spec.s.map(s => v[s.k]));
        c.spec.s.forEach(s => {
          const b = c.el.querySelector(`[data-k="${s.k}"]`);
          if (b && v[s.k] != null) b.textContent = Math.abs(v[s.k]) >= 10 ? Math.round(v[s.k]) : v[s.k].toFixed(2);
        });
      });
    };
    es.onerror = () => { const p = $("#tlive"); if (p) { p.textContent = "riconnetto…"; p.style.color = "#e07b5a"; } };
    card._es = es;
  },
  status(card) {
    card.innerHTML = '<h3>🧊 Stato sistema</h3><div class="rows" id="srows">…</div>';
    const fill = async () => {
      try {
        const s = await (await api("/api/status")).json();
        const row = (a, b) => `<div class="r"><span>${a}</span><span>${b || "–"}</span></div>`;
        $("#srows", card).innerHTML =
          row("Host", s.host) + row("IP", s.ip) + row("Kernel", s.kernel) +
          row("Uptime", s.uptime) + row("CU attive", s.cu) +
          row("RAM", s.ram_used_mb ? `${s.ram_used_mb} / ${s.ram_total_mb} MB` : "") +
          row("Disco /", s.disk_used ? `${s.disk_used} / ${s.disk_total} (${s.disk_pct})` : "") +
          row("Freeze rilevati", s.freezes);
      } catch (e) {}
    };
    fill(); card._iv = setInterval(fill, 5000);
  },
  async tuner(card) {
    card.innerHTML = '<h3>🎛️ Controlli</h3><div id="tk">…</div>';
    let d; try { d = await (await api("/api/tuner")).json(); } catch (e) { return; }
    const presets = (d.presets || []).map(p =>
      `<button class="dbtn" data-preset="${p.name}" title="${(p.desc || '').replace(/"/g, '')}">${p.name}</button>`).join("");
    $("#tk", card).innerHTML =
      `<div class="grp"><div class="gl">Preset</div><div class="brow">${presets}</div></div>` +
      `<div class="grp"><div class="gl">Governor GPU</div><div class="brow">` +
      `<button class="dbtn" data-gov="balanced">Bilanciato</button><button class="dbtn" data-gov="performance">Performance</button></div></div>` +
      `<div class="grp"><div class="gl">Ventola</div><div class="brow">` +
      `<button class="dbtn" data-fan="auto">Auto</button>` +
      `<input id="fanp" type="range" min="20" max="100" value="60" style="flex:1">` +
      `<button class="dbtn" data-fanmanual="1">Manuale</button></div></div>`;
    card.querySelectorAll("[data-preset]").forEach(b => b.onclick = () =>
      action("/api/tuner/preset", { name: b.dataset.preset }, "Preset " + b.dataset.preset + " applicato"));
    card.querySelectorAll("[data-gov]").forEach(b => b.onclick = () =>
      action("/api/tuner/govmode", { mode: b.dataset.gov }, "Governor: " + b.dataset.gov));
    card.querySelector("[data-fan]").onclick = () => action("/api/tuner/fan", { mode: "auto" }, "Ventola: auto");
    card.querySelector("[data-fanmanual]").onclick = () =>
      action("/api/tuner/fan", { mode: "manual", pct: +$("#fanp", card).value }, "Ventola: " + $("#fanp", card).value + "%");
  },
  power(card) {
    card.innerHTML = '<h3>🔌 Alimentazione</h3><div class="brow">' +
      '<button class="dbtn danger" id="reboot">↻ Riavvia</button>' +
      '<button class="dbtn danger" id="poweroff">⏻ Spegni</button></div>' +
      '<div class="stub" style="margin-top:8px">Richiede conferma.</div>';
    $("#reboot", card).onclick = () => { if (confirm("Riavviare la BC-250?")) action("/api/power", { action: "reboot" }, "Riavvio…"); };
    $("#poweroff", card).onclick = () => { if (confirm("Spegnere la BC-250?")) action("/api/power", { action: "poweroff" }, "Spegnimento…"); };
  },
  logs(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>📜 Log <select id="lw" class="dsel">' +
      '<option value="journal">journal</option><option value="kernel">kernel</option><option value="freeze">freeze</option>' +
      '</select> <button class="dbtn" id="lref">⟳</button></h3><pre class="logbox" id="lb">…</pre>';
    const load = async () => {
      try { const j = await (await api("/api/logs?n=200&which=" + $("#lw", card).value)).json();
        const lb = $("#lb", card); lb.textContent = (j.lines || []).join("\n") || "(vuoto)"; lb.scrollTop = lb.scrollHeight; } catch (e) {}
    };
    $("#lw", card).onchange = load; $("#lref", card).onclick = load; load();
  },
  launcher(card) {
    card.innerHTML = '<h3>🚀 Avvio app</h3><div class="brow">' +
      [["console", "🎮 Console"], ["monitor", "📊 Telemetry"], ["tuner", "🎛️ Tuner"], ["hub", "📦 Hub"], ["ai", "🧠 AI"]]
        .map(([k, l]) => `<button class="dbtn" data-app="${k}">${l}</button>`).join("") + "</div>" +
      '<div class="stub" style="margin-top:8px">Si apre sullo schermo della scheda.</div>';
    card.querySelectorAll("[data-app]").forEach(b => b.onclick = () =>
      action("/api/launch", { what: b.dataset.app }, "Avviato: " + b.dataset.app));
  },
  recording(card) {
    card.innerHTML = '<h3>⏺️ Registrazioni</h3><div class="brow"><button class="dbtn" id="rec">● REC</button></div><div id="rl" class="rows"></div>';
    const refresh = async () => {
      try {
        const j = await (await api("/api/rec/list")).json();
        const b = $("#rec", card);
        b.textContent = j.recording ? "■ STOP" : "● REC";
        b.classList.toggle("danger", !!j.recording); b.dataset.on = j.recording ? "1" : "";
        $("#rl", card).innerHTML = (j.recordings || []).slice(0, 8).map(r =>
          `<div class="r"><a href="/api/rec/get?f=${encodeURIComponent(r.name)}">${r.name}</a><span>${(r.size / 1024).toFixed(0)} KB</span></div>`).join("") || '<div class="stub">Nessuna registrazione.</div>';
      } catch (e) {}
    };
    $("#rec", card).onclick = async () => {
      const on = $("#rec", card).dataset.on;
      await action(on ? "/api/rec/stop" : "/api/rec/start", {}, on ? "Registrazione salvata" : "Registrazione avviata");
      refresh();
    };
    refresh(); card._iv = setInterval(refresh, 4000);
  },
  kvm(card) {
    card.innerHTML = '<h3>🖥️ Desktop (KVM)</h3><div class="brow"><button class="dbtn" id="kvmgo">▶ Avvia desktop remoto</button></div>' +
      '<div class="stub" id="kvmi" style="margin-top:8px">Schermo, tastiera e mouse della scheda nel browser.</div>';
    $("#kvmgo", card).onclick = async () => {
      const j = await action("/api/kvm/start", {}, "Desktop pronto");
      if (j && j.url) { window.open(j.url, "_blank"); $("#kvmi", card).innerHTML = "Aperto in nuova scheda. Password VNC: <b>" + j.password + "</b>"; }
    };
  },
  terminal(card) {
    card.innerHTML = '<h3>⌨️ Terminale</h3><div class="brow"><button class="dbtn" id="tgo">▶ Apri terminale</button></div>' +
      '<div class="stub" id="ti" style="margin-top:8px">Shell della scheda nel browser.</div>';
    $("#tgo", card).onclick = async () => {
      const j = await action("/api/terminal/start", {}, "Terminale pronto");
      if (j && j.url) { window.open(j.url, "_blank"); $("#ti", card).innerHTML = "Aperto. Login: utente <b>" + j.user + "</b> · token <b>" + j.token + "</b>"; }
    };
  },
  _stub(card, mod) {
    card.innerHTML = `<h3>${mod.icon} ${mod.name}</h3><div class="stub">Modulo attivo — interfaccia in arrivo.</div>`;
  },
};

async function buildDashboard() {
  $("#login").style.display = "none"; $("#app").style.display = "block";
  let data; try { data = await (await api("/api/modules")).json(); } catch (e) { return showLogin(); }
  $("#host").textContent = data.host || "";
  const grid = $("#grid"); grid.innerHTML = "";
  (data.modules || []).forEach(mod => {
    const card = document.createElement("div"); card.className = "mod";
    (RENDER[mod.id] || ((c) => RENDER._stub(c, mod)))(card, mod);
    grid.appendChild(card);
  });
}

function showLogin() {
  $("#app").style.display = "none"; $("#login").style.display = "grid"; $("#u").focus();
}

$("#lform").addEventListener("submit", async ev => {
  ev.preventDefault(); $("#lerr").textContent = "";
  const r = await api("/api/login", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user: $("#u").value, pass: $("#p").value }),
  });
  if (r.ok) { $("#p").value = ""; buildDashboard(); }
  else { const j = await r.json().catch(() => ({})); $("#lerr").textContent = j.error || "accesso negato"; }
});

$("#logout").addEventListener("click", async () => {
  await api("/api/logout", { method: "POST" }); location.reload();
});

(async () => {
  try {
    const r = await api("/api/me");
    if (r.ok) buildDashboard(); else showLogin();
  } catch (e) { showLogin(); }
})();
