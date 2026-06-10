"use strict";
// SkillFishOS Remote Manager - dynamic, module-composed dashboard frontend (IT/EN).
const $ = (s, r = document) => r.querySelector(s);
const api = (p, opt) => fetch(p, Object.assign({ credentials: "same-origin" }, opt));
const post = (p, body) => api(p, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });

// ---------------- i18n ----------------
let LANG = localStorage.getItem("sflang") || ((navigator.language || "en").toLowerCase().startsWith("it") ? "it" : "en");
const STR = {
  login_sub: { it: "SkillFishOS · accedi con le credenziali di sistema", en: "SkillFishOS · sign in with your system credentials" },
  user: { it: "Utente", en: "User" }, pass: { it: "Password", en: "Password" },
  enter: { it: "Entra", en: "Sign in" }, denied: { it: "accesso negato", en: "access denied" },
  logout: { it: "Esci", en: "Log out" }, neterr: { it: "errore di rete", en: "network error" },
  copied: { it: "Copiato", en: "Copied" }, done: { it: "fatto", en: "done" },
  g_monitor: { it: "Monitoraggio", en: "Monitoring" }, g_control: { it: "Controllo", en: "Control" },
  g_remote: { it: "Accesso remoto", en: "Remote access" }, g_ai: { it: "Intelligenza artificiale", en: "AI" },
  g_other: { it: "Altro", en: "Other" },
  // telemetry
  t_temp: { it: "Temperatura", en: "Temperature" }, t_load: { it: "Carico", en: "Load" },
  t_freq: { it: "Frequenza", en: "Frequency" }, t_pow: { it: "Potenza", en: "Power" },
  t_volt: { it: "Voltaggio", en: "Voltage" }, t_fan: { it: "Ventola", en: "Fan" }, live: { it: "live", en: "live" },
  // status
  s_you: { it: "Sei connesso a", en: "Connected to" }, s_host: { it: "Host", en: "Host" },
  s_ip: { it: "IP (rotta)", en: "IP (route)" }, s_kernel: { it: "Kernel", en: "Kernel" },
  s_up: { it: "Uptime", en: "Uptime" }, s_cu: { it: "CU attive", en: "Active CUs" }, s_ram: { it: "RAM", en: "RAM" },
  s_disk: { it: "Disco /", en: "Disk /" }, s_frz: { it: "Freeze rilevati", en: "Freezes detected" },
  // tuner
  c_preset: { it: "Preset", en: "Presets" }, c_gov: { it: "Governor GPU", en: "GPU governor" },
  c_bal: { it: "Bilanciato", en: "Balanced" }, c_perf: { it: "Performance", en: "Performance" },
  c_fan: { it: "Ventola", en: "Fan" }, c_auto: { it: "Auto", en: "Auto" }, c_man: { it: "Manuale", en: "Manual" },
  c_applied: { it: "Preset {x} applicato", en: "Preset {x} applied" },
  // power
  p_reboot: { it: "Riavvia", en: "Reboot" }, p_off: { it: "Spegni", en: "Shut down" },
  p_conf: { it: "Richiede conferma.", en: "Asks for confirmation." },
  p_qreb: { it: "Riavviare la BC-250?", en: "Reboot the BC-250?" }, p_qoff: { it: "Spegnere la BC-250?", en: "Shut down the BC-250?" },
  p_rebing: { it: "Riavvio…", en: "Rebooting…" }, p_offing: { it: "Spegnimento…", en: "Shutting down…" },
  // logs / launcher / rec
  l_refresh: { it: "aggiorna", en: "refresh" }, empty: { it: "(vuoto)", en: "(empty)" },
  la_hint: { it: "Si apre sullo schermo della scheda.", en: "Opens on the board's screen." },
  la_started: { it: "Avviato: {x}", en: "Launched: {x}" },
  r_none: { it: "Nessuna registrazione.", en: "No recordings." }, r_saved: { it: "Registrazione salvata", en: "Recording saved" },
  r_started: { it: "Registrazione avviata", en: "Recording started" },
  // kvm / terminal
  k_open: { it: "▶ Apri desktop remoto", en: "▶ Open remote desktop" },
  k_hint: { it: "Schermo, tastiera e mouse della scheda — stessa sessione, nessuna password in più.", en: "Screen, keyboard and mouse of the board — same session, no extra password." },
  k_ready: { it: "Desktop pronto", en: "Desktop ready" }, k_vncpw: { it: "Aperto. Password VNC (se richiesta): ", en: "Opened. VNC password (if asked): " },
  term_open: { it: "▶ Apri terminale", en: "▶ Open terminal" },
  term_hint: { it: "Shell della scheda — stessa sessione, nessuna password in più.", en: "Board shell — same session, no extra password." },
  // ai
  ai_engine: { it: "Motore (Ollama)", en: "Engine (Ollama)" }, ai_on: { it: "● acceso", en: "● on" }, ai_off: { it: "○ spento", en: "○ off" },
  ai_start: { it: "▶ Accendi AI", en: "▶ Turn on AI" }, ai_stop: { it: "■ Spegni AI", en: "■ Turn off AI" },
  ai_open: { it: "Apri OpenWebUI ↗", en: "Open OpenWebUI ↗" }, ai_ready: { it: "● pronto", en: "● ready" },
  ai_hint: { it: "Lo stack gira sulla GPU: spegnilo quando giochi.", en: "The stack runs on the GPU: turn it off when gaming." },
  ai_starting: { it: "Avvio AI… (può richiedere un minuto)", en: "Starting AI… (may take a minute)" }, ai_stopping: { it: "Spengo AI", en: "Stopping AI" },
  // wol
  w_wol: { it: "Wake-on-LAN", en: "Wake-on-LAN" }, w_en: { it: "● abilitato", en: "● enabled" }, w_dis: { it: "○ disabilitato", en: "○ disabled" },
  w_enbtn: { it: "Abilita WoL", en: "Enable WoL" }, w_disbtn: { it: "Disabilita WoL", en: "Disable WoL" },
  w_wake: { it: "Sveglia un altro dispositivo", en: "Wake another device" }, w_send: { it: "Invia", en: "Send" }, w_sent: { it: "Magic packet inviato", en: "Magic packet sent" },
  w_sched: { it: "Programma spegnimento/riavvio", en: "Schedule power off/reboot" }, w_cancel: { it: "Annulla", en: "Cancel" },
  w_qreb: { it: "Riavviare tra {x} min?", en: "Reboot in {x} min?" }, w_qoff: { it: "Spegnere tra {x} min?", en: "Shut down in {x} min?" },
  w_updated: { it: "WoL aggiornato", en: "WoL updated" }, w_rsched: { it: "Riavvio programmato", en: "Reboot scheduled" }, w_osched: { it: "Spegnimento programmato", en: "Shutdown scheduled" }, w_canc: { it: "Programmazione annullata", en: "Schedule cancelled" },
  // rules
  ru_throttle: { it: "Auto-throttle a Stock se troppo caldo", en: "Auto-throttle to Stock when too hot" },
  ru_thresh: { it: "Soglia", en: "Threshold" }, ru_last: { it: "Ultima azione", en: "Last action" },
  ru_on: { it: "● attivo", en: "● on" }, ru_off: { it: "○ spento", en: "○ off" }, ru_enable: { it: "Attiva", en: "Enable" }, ru_disable: { it: "Disattiva", en: "Disable" },
  ru_set: { it: "Imposta", en: "Set" }, ru_updated: { it: "Regola aggiornata", en: "Rule updated" }, ru_setdone: { it: "Soglia impostata", en: "Threshold set" },
  ru_frame: { it: "Ultimo fotogramma dello schermo", en: "Last screen frame" }, ru_noframe: { it: "Nessun fotogramma ancora (attiva il modulo e attendi ~20s).", en: "No frame yet (enable the module and wait ~20s)." },
  // aiops
  ao_q: { it: "Domanda (opzionale): perché si è bloccata?", en: "Question (optional): why did it freeze?" },
  ao_btn: { it: "Diagnostica", en: "Diagnose" }, ao_running: { it: "Analisi in corso col modello locale… (può richiedere un minuto)", en: "Analyzing with the local model… (may take a minute)" },
  ao_hint: { it: "Il modello locale (Ollama) legge log e telemetria e spiega cosa succede. Richiede il motore AI acceso.", en: "The local model (Ollama) reads logs and telemetry and explains what's going on. Needs the AI engine on." },
  ao_none: { it: "(nessuna risposta)", en: "(no answer)" }, err: { it: "Errore: ", en: "Error: " },
};
function T(k, vars) {
  let s = (STR[k] && STR[k][LANG]) || (STR[k] && STR[k].en) || k;
  if (vars) for (const v in vars) s = s.replace("{" + v + "}", vars[v]);
  return s;
}

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
  try { const j = await (await post(p, body)).json(); toast(j.ok === false ? (j.error || T("err").trim()) : (okmsg || T("done")), j.ok !== false); return j; }
  catch (e) { toast(T("neterr"), false); }
}
// centered modal with an embedded web app (same-origin via the dashboard proxy)
function openFrame(title, url) {
  let m = $("#frame");
  if (!m) {
    m = document.createElement("div"); m.id = "frame";
    m.innerHTML = '<div class="fr-box"><div class="fr-bar"><span class="fr-title"></span><span class="fr-sp"></span><button class="fr-btn" id="fr-pop" title="Nuova scheda">⤢</button><button class="fr-btn" id="fr-x">✕</button></div><iframe class="fr-if" allow="clipboard-read; clipboard-write"></iframe></div>';
    document.body.appendChild(m);
    const close = () => { m.style.display = "none"; $(".fr-if", m).src = "about:blank"; };
    $("#fr-x", m).onclick = close;
    $("#fr-pop", m).onclick = () => window.open($(".fr-if", m).dataset.url, "_blank");
    m.addEventListener("click", e => { if (e.target === m) close(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && m.style.display === "flex") close(); });
  }
  $(".fr-title", m).textContent = title;
  const f = $(".fr-if", m); f.dataset.url = url; f.src = url; m.style.display = "flex";
}
// settings modal: pick which modules the web dashboard exposes
async function openSettings() {
  const it = LANG === "it";
  let d; try { d = await (await api("/api/config")).json(); } catch (e) { return; }
  let m = $("#settings");
  if (!m) { m = document.createElement("div"); m.id = "settings"; m.className = "overlay"; document.body.appendChild(m); m.addEventListener("click", e => { if (e.target === m) m.style.display = "none"; }); }
  const rows = (d.catalogue || []).map(c => `<label class="setrow"><input type="checkbox" data-m="${c.id}" ${d.modules[c.id] ? "checked" : ""}> ${c.icon} ${it ? c.name : (c.name_en || c.name)}</label>`).join("");
  m.innerHTML = '<div class="setbox"><div class="fr-bar"><span class="fr-title">' + (it ? "Moduli esposti" : "Exposed modules") + '</span><span class="fr-sp"></span><button class="fr-btn" id="set-x">✕</button></div><div class="setgrid">' + rows + "</div></div>";
  m.style.display = "flex";
  $("#set-x", m).onclick = () => m.style.display = "none";
  m.querySelectorAll("[data-m]").forEach(cb => cb.onchange = async () => { await action("/api/config", { module: cb.dataset.m, on: cb.checked }, it ? "Aggiornato" : "Updated"); buildDashboard(); });
}
function copyable(value) {
  return '<span class="cpw"><b style="user-select:all">' + value + '</b> <button class="cpy" type="button" data-cp="' +
    String(value).replace(/"/g, "&quot;") + '" title="' + T("copied") + '">📋</button></span>';
}
document.addEventListener("click", (e) => {
  const b = e.target.closest(".cpy"); if (!b) return;
  const v = b.dataset.cp;
  (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(() => toast(T("copied")))
    .catch(() => { const t = document.createElement("textarea"); t.value = v; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); toast(T("copied")); } catch (_) {} t.remove(); });
});

// ---------------- charts ----------------
class Mini {
  constructor(canvas, series) { this.c = canvas; this.series = series; this.data = series.map(() => []); this.max = 90; }
  push(vals) { vals.forEach((v, i) => { const d = this.data[i]; d.push(v == null ? (d.length ? d[d.length - 1] : 0) : v); if (d.length > this.max) d.shift(); }); this.draw(); }
  draw() {
    const cv = this.c, dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
    if (cv.width !== w * dpr) { cv.width = w * dpr; cv.height = h * dpr; }
    const x = cv.getContext("2d"); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
    let all = []; this.data.forEach(d => all = all.concat(d)); if (!all.length) return;
    let lo = Math.min(...all), hi = Math.max(...all); if (hi - lo < 1e-6) hi = lo + 1; const m = (hi - lo) * 0.15; lo -= m; hi += m;
    this.data.forEach((d, i) => { if (d.length < 2) return; x.beginPath(); d.forEach((v, j) => { const px = w * j / (d.length - 1), py = h - h * (v - lo) / (hi - lo); j ? x.lineTo(px, py) : x.moveTo(px, py); }); x.strokeStyle = this.series[i].c; x.lineWidth = 1.6; x.lineJoin = "round"; x.stroke(); });
  }
}
const TELEM = [
  { t: "t_temp", u: "°C", s: [{ k: "cpu_temp", l: "CPU", c: "#e8c878" }, { k: "gpu_temp", l: "GPU", c: "#e07b39" }] },
  { t: "t_load", u: "%", s: [{ k: "cpu_load", l: "CPU", c: "#5fd24f" }, { k: "gpu_util", l: "GPU", c: "#49b6e0" }] },
  { t: "t_freq", u: "MHz", s: [{ k: "cpu_mhz", l: "CPU", c: "#9bd24f" }, { k: "gpu_freq", l: "GPU", c: "#49b6e0" }] },
  { t: "t_pow", u: "W", s: [{ k: "gpu_power", l: "GPU", c: "#e0d24f" }] },
  { t: "t_volt", u: "mV", s: [{ k: "gpu_mv", l: "GPU", c: "#c98be0" }, { k: "cpu_mv", l: "CPU", c: "#e8a878" }] },
  { t: "t_fan", u: "RPM", s: [{ k: "fan", l: "FAN", c: "#d8a849" }] },
];

// ---------------- module groups ----------------
const GROUPS = [
  { t: "g_monitor", mods: ["telemetry", "status", "rules", "logs"] },
  { t: "g_control", mods: ["tuner", "power", "recording", "launcher"] },
  { t: "g_remote", mods: ["kvm", "terminal", "wol", "zerotier"] },
  { t: "g_ai", mods: ["ai", "aiops"] },
  { t: "g_other", mods: ["gamestream"] },
];

const RENDER = {
  telemetry(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>📊 ' + (LANG === "it" ? "Telemetria" : "Telemetry") + ' <span class="pill" id="tlive">' + T("live") + '</span></h3><div class="charts"></div>';
    const box = $(".charts", card); const charts = [];
    TELEM.forEach(spec => {
      const el = document.createElement("div"); el.className = "chart";
      const labs = spec.s.map(s => `<span style="color:${s.c}">${s.l} <b class="val" data-k="${s.k}">–</b></span>`).join(" ");
      el.innerHTML = `<div class="lab"><span>${T(spec.t)} (${spec.u})</span><span>${labs}</span></div><canvas></canvas>`;
      box.appendChild(el); charts.push({ spec, m: new Mini($("canvas", el), spec.s), el });
    });
    const es = new EventSource("/api/telemetry");
    es.onmessage = ev => { let v; try { v = JSON.parse(ev.data); } catch (e) { return; }
      charts.forEach(c => { c.m.push(c.spec.s.map(s => v[s.k])); c.spec.s.forEach(s => { const b = c.el.querySelector(`[data-k="${s.k}"]`); if (b && v[s.k] != null) b.textContent = Math.abs(v[s.k]) >= 10 ? Math.round(v[s.k]) : v[s.k].toFixed(2); }); });
    };
    card._es = es;
  },
  status(card) {
    card.innerHTML = "<h3>🧊 " + (LANG === "it" ? "Stato sistema" : "System status") + '</h3><div class="rows" id="srows">…</div>';
    const fill = async () => { try { const s = await (await api("/api/status")).json();
      const row = (a, b) => `<div class="r"><span>${a}</span><span>${b || "–"}</span></div>`;
      $("#srows", card).innerHTML = row(T("s_you"), s.you) + row(T("s_host"), s.host) + row(T("s_ip"), s.ip) + row(T("s_kernel"), s.kernel) +
        row(T("s_up"), s.uptime) + row(T("s_cu"), s.cu) + row(T("s_ram"), s.ram_used_mb ? `${s.ram_used_mb} / ${s.ram_total_mb} MB` : "") +
        row(T("s_disk"), s.disk_used ? `${s.disk_used} / ${s.disk_total} (${s.disk_pct})` : "") + row(T("s_frz"), s.freezes);
    } catch (e) {} };
    fill(); card._iv = setInterval(fill, 5000);
  },
  async tuner(card) {
    card.innerHTML = "<h3>🎛️ " + (LANG === "it" ? "Controlli" : "Controls") + '</h3><div id="tk">…</div>';
    let d; try { d = await (await api("/api/tuner")).json(); } catch (e) { return; }
    const presets = (d.presets || []).map(p => `<button class="dbtn" data-preset="${p.name}" title="${(p.desc || "").replace(/"/g, "")}">${p.name}</button>`).join("");
    $("#tk", card).innerHTML =
      `<div class="grp"><div class="gl">${T("c_preset")}</div><div class="brow">${presets}</div></div>` +
      `<div class="grp"><div class="gl">${T("c_gov")}</div><div class="brow"><button class="dbtn" data-gov="balanced">${T("c_bal")}</button><button class="dbtn" data-gov="performance">${T("c_perf")}</button></div></div>` +
      `<div class="grp"><div class="gl">${T("c_fan")}</div><div class="brow"><button class="dbtn" data-fan="auto">${T("c_auto")}</button><input id="fanp" type="range" min="20" max="100" value="60" style="flex:1"><button class="dbtn" data-fanmanual="1">${T("c_man")}</button></div></div>`;
    card.querySelectorAll("[data-preset]").forEach(b => b.onclick = () => action("/api/tuner/preset", { name: b.dataset.preset }, T("c_applied", { x: b.dataset.preset })));
    card.querySelectorAll("[data-gov]").forEach(b => b.onclick = () => action("/api/tuner/govmode", { mode: b.dataset.gov }, "Governor: " + b.dataset.gov));
    card.querySelector("[data-fan]").onclick = () => action("/api/tuner/fan", { mode: "auto" }, T("c_fan") + ": " + T("c_auto"));
    card.querySelector("[data-fanmanual]").onclick = () => action("/api/tuner/fan", { mode: "manual", pct: +$("#fanp", card).value }, T("c_fan") + ": " + $("#fanp", card).value + "%");
  },
  power(card) {
    card.innerHTML = "<h3>🔌 " + (LANG === "it" ? "Alimentazione" : "Power") + '</h3><div class="brow"><button class="dbtn danger" id="reboot">↻ ' + T("p_reboot") + '</button><button class="dbtn danger" id="poweroff">⏻ ' + T("p_off") + '</button></div><div class="stub" style="margin-top:8px">' + T("p_conf") + '</div>';
    $("#reboot", card).onclick = () => { if (confirm(T("p_qreb"))) action("/api/power", { action: "reboot" }, T("p_rebing")); };
    $("#poweroff", card).onclick = () => { if (confirm(T("p_qoff"))) action("/api/power", { action: "poweroff" }, T("p_offing")); };
  },
  logs(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>📜 Log <select id="lw" class="dsel"><option value="journal">journal</option><option value="kernel">kernel</option><option value="freeze">freeze</option></select> <button class="dbtn" id="lref">⟳</button></h3><pre class="logbox" id="lb">…</pre>';
    const load = async () => { try { const j = await (await api("/api/logs?n=200&which=" + $("#lw", card).value)).json(); const lb = $("#lb", card); lb.textContent = (j.lines || []).join("\n") || T("empty"); lb.scrollTop = lb.scrollHeight; } catch (e) {} };
    $("#lw", card).onchange = load; $("#lref", card).onclick = load; load();
  },
  launcher(card) {
    card.innerHTML = "<h3>🚀 " + (LANG === "it" ? "Avvio app" : "Launcher") + '</h3><div class="brow">' +
      [["console", "🎮 Console"], ["monitor", "📊 Telemetry"], ["tuner", "🎛️ Tuner"], ["hub", "📦 Hub"], ["ai", "🧠 AI"]].map(([k, l]) => `<button class="dbtn" data-app="${k}">${l}</button>`).join("") + "</div>" +
      '<div class="stub" style="margin-top:8px">' + T("la_hint") + "</div>";
    card.querySelectorAll("[data-app]").forEach(b => b.onclick = () => action("/api/launch", { what: b.dataset.app }, T("la_started", { x: b.dataset.app })));
  },
  recording(card) {
    card.innerHTML = "<h3>⏺️ " + (LANG === "it" ? "Registrazioni" : "Recordings") + '</h3><div class="brow"><button class="dbtn" id="rec">● REC</button></div><div id="rl" class="rows"></div>';
    const refresh = async () => { try { const j = await (await api("/api/rec/list")).json(); const b = $("#rec", card);
      b.textContent = j.recording ? "■ STOP" : "● REC"; b.classList.toggle("danger", !!j.recording); b.dataset.on = j.recording ? "1" : "";
      $("#rl", card).innerHTML = (j.recordings || []).slice(0, 8).map(r => `<div class="r"><a href="/api/rec/get?f=${encodeURIComponent(r.name)}">${r.name}</a><span>${(r.size / 1024).toFixed(0)} KB</span></div>`).join("") || '<div class="stub">' + T("r_none") + "</div>";
    } catch (e) {} };
    $("#rec", card).onclick = async () => { const on = $("#rec", card).dataset.on; await action(on ? "/api/rec/stop" : "/api/rec/start", {}, on ? T("r_saved") : T("r_started")); refresh(); };
    refresh(); card._iv = setInterval(refresh, 4000);
  },
  kvm(card) {
    card.innerHTML = '<h3>🖥️ Desktop (KVM)</h3><div class="brow"><button class="dbtn" id="kvmgo">' + T("k_open") + '</button></div><div class="stub" id="kvmi" style="margin-top:8px">' + T("k_hint") + "</div>";
    $("#kvmgo", card).onclick = async () => { const j = await action("/api/kvm/start", {}, T("k_ready"));
      if (j && j.password != null) { openFrame("Desktop (KVM)", "/kvm/vnc.html?autoconnect=1&resize=scale&reconnect=1&path=" + encodeURIComponent("kvm/websockify") + "&password=" + encodeURIComponent(j.password)); $("#kvmi", card).innerHTML = T("k_vncpw") + copyable(j.password); } };
  },
  terminal(card) {
    card.innerHTML = "<h3>⌨️ " + (LANG === "it" ? "Terminale" : "Terminal") + '</h3><div class="brow"><button class="dbtn" id="tgo">' + T("term_open") + '</button></div><div class="stub" style="margin-top:8px">' + T("term_hint") + "</div>";
    $("#tgo", card).onclick = () => openFrame(LANG === "it" ? "Terminale" : "Terminal", "/terminal/");
  },
  ai(card) {
    const it = LANG === "it";
    card.innerHTML = "<h3>🧠 AI / OpenWebUI</h3><div id=\"ai\">…</div>";
    const refresh = async () => { let s; try { s = await (await api("/api/ai")).json(); } catch (e) { return; }
      const models = (s.models || []).map(mn => `<span class="pill" style="display:inline-block;margin:2px">${mn}</span>`).join(" ") || `<span class="stub">${it ? "nessun modello installato" : "no models installed"}</span>`;
      $("#ai", card).innerHTML = '<div class="rows"><div class="r"><span>' + T("ai_engine") + "</span><span>" + (s.running ? T("ai_on") : T("ai_off")) + '</span></div><div class="r"><span>OpenWebUI</span><span>' + (s.webui ? T("ai_ready") : T("ai_off")) + "</span></div></div>" +
        '<div class="brow" style="margin-top:10px">' + (s.running ? '<button class="dbtn danger" id="aistop">' + T("ai_stop") + "</button>" : '<button class="dbtn" id="aistart">' + T("ai_start") + "</button>") +
        '<button class="dbtn" id="aichat"' + (s.running ? "" : " disabled") + ">💬 " + (it ? "Chat" : "Chat") + "</button>" +
        '<button class="dbtn" id="aiweb"' + (s.webui ? "" : " disabled") + ">" + T("ai_open") + "</button></div>" +
        '<div class="gl" style="margin-top:12px">' + (it ? "Modelli installati" : "Installed models") + '</div><div style="margin-top:4px">' + models + "</div>" +
        '<div class="brow" style="margin-top:10px"><input id="aipm" class="dsel" placeholder="' + (it ? "scarica modello (es. qwen3:14b)" : "pull model (e.g. qwen3:14b)") + '" style="flex:1"><button class="dbtn" id="aipull"' + (s.running ? "" : " disabled") + ">" + (it ? "Scarica" : "Pull") + "</button></div>" +
        '<div class="stub" style="margin-top:8px">' + T("ai_hint") + "</div>";
      if ($("#aistart", card)) $("#aistart", card).onclick = async () => { await action("/api/ai/start", {}, T("ai_starting")); setTimeout(refresh, 4000); };
      if ($("#aistop", card)) $("#aistop", card).onclick = async () => { await action("/api/ai/stop", {}, T("ai_stopping")); setTimeout(refresh, 2000); };
      if ($("#aichat", card)) $("#aichat", card).onclick = () => openFrame("SkillFishOS AI", "/static/aichat.html");
      if ($("#aiweb", card)) $("#aiweb", card).onclick = () => window.open("http://" + location.hostname + ":" + s.webui_port, "_blank");
      if ($("#aipull", card)) $("#aipull", card).onclick = async () => { if ($("#aipm", card).value.trim()) { await action("/api/ai/pull", { model: $("#aipm", card).value }, it ? "Download avviato…" : "Download started…"); $("#aipm", card).value = ""; } };
    };
    refresh(); card._iv = setInterval(refresh, 5000);
  },
  wol(card) {
    card.innerHTML = "<h3>🔋 Power schedule / WoL</h3><div id=\"wol\">…</div>";
    const refresh = async () => { let s; try { s = await (await api("/api/wol")).json(); } catch (e) { return; }
      $("#wol", card).innerHTML = '<div class="rows"><div class="r"><span>NIC</span><span>' + s.nic + '</span></div><div class="r"><span>MAC</span><span>' + copyable(s.mac) + '</span></div><div class="r"><span>' + T("w_wol") + "</span><span>" + (s.wol_enabled ? T("w_en") : T("w_dis")) + "</span></div></div>" +
        '<div class="brow" style="margin-top:10px"><button class="dbtn" id="wolt">' + (s.wol_enabled ? T("w_disbtn") : T("w_enbtn")) + "</button></div>" +
        '<div class="gl" style="margin-top:12px">' + T("w_wake") + '</div><div class="brow"><input id="wmac" class="dsel" placeholder="AA:BB:CC:DD:EE:FF" style="flex:1"><button class="dbtn" id="wsend">' + T("w_send") + "</button></div>" +
        '<div class="gl" style="margin-top:12px">' + T("w_sched") + '</div><div class="brow"><input id="wmin" class="dsel" type="number" value="10" min="1" style="width:64px"> min <button class="dbtn" id="wreb">↻ ' + T("p_reboot") + '</button><button class="dbtn danger" id="woff">⏻ ' + T("p_off") + '</button><button class="dbtn" id="wcan">' + T("w_cancel") + "</button></div>";
      $("#wolt", card).onclick = async () => { await action("/api/wol/enable", { on: !s.wol_enabled }, T("w_updated")); setTimeout(refresh, 800); };
      $("#wsend", card).onclick = () => action("/api/wol/send", { mac: $("#wmac", card).value }, T("w_sent"));
      $("#wreb", card).onclick = () => { if (confirm(T("w_qreb", { x: $("#wmin", card).value }))) action("/api/wol/schedule", { action: "reboot", minutes: +$("#wmin", card).value }, T("w_rsched")); };
      $("#woff", card).onclick = () => { if (confirm(T("w_qoff", { x: $("#wmin", card).value }))) action("/api/wol/schedule", { action: "poweroff", minutes: +$("#wmin", card).value }, T("w_osched")); };
      $("#wcan", card).onclick = () => action("/api/wol/schedule", { action: "cancel" }, T("w_canc"));
    };
    refresh();
  },
  rules(card) {
    card.innerHTML = "<h3>⚙️ " + (LANG === "it" ? "Regole auto" : "Auto rules") + '</h3><div id="ru">…</div>';
    const refresh = async () => { let s; try { s = await (await api("/api/rules")).json(); } catch (e) { return; }
      $("#ru", card).innerHTML = '<div class="rows"><div class="r"><span>' + T("ru_throttle") + "</span><span>" + (s.enabled ? T("ru_on") : T("ru_off")) + '</span></div><div class="r"><span>' + T("ru_thresh") + "</span><span>" + s.temp_limit + " °C</span></div>" + (s.last_action ? '<div class="r"><span>' + T("ru_last") + "</span><span>" + s.last_action + "</span></div>" : "") + "</div>" +
        '<div class="brow" style="margin-top:10px"><button class="dbtn" id="rtog">' + (s.enabled ? T("ru_disable") : T("ru_enable")) + '</button><input id="rlim" class="dsel" type="number" min="70" max="100" value="' + s.temp_limit + '" style="width:64px"> °C <button class="dbtn" id="rset">' + T("ru_set") + "</button></div>";
      $("#rtog", card).onclick = async () => { await action("/api/rules", { enabled: !s.enabled }, T("ru_updated")); setTimeout(refresh, 500); };
      $("#rset", card).onclick = async () => { await action("/api/rules", { temp_limit: +$("#rlim", card).value }, T("ru_setdone")); setTimeout(refresh, 500); };
    };
    refresh(); card._iv = setInterval(refresh, 15000);
  },
  aiops(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>🩺 AI-Ops</h3><div class="brow"><input id="aq" class="dsel" placeholder="' + T("ao_q") + '" style="flex:1"><button class="dbtn" id="adg">' + T("ao_btn") + '</button></div><div class="logbox" id="aout" style="margin-top:8px;display:none"></div><div class="stub" style="margin-top:8px">' + T("ao_hint") + "</div>";
    $("#adg", card).onclick = async () => { const out = $("#aout", card); out.style.display = "block"; out.textContent = T("ao_running");
      const j = await (await post("/api/aiops/diagnose", { question: $("#aq", card).value })).json().catch(() => ({})); out.textContent = j.ok ? (j.answer || T("ao_none")) : (T("err") + (j.error || "")); };
  },
  zerotier(card) {
    const it = LANG === "it";
    card.innerHTML = "<h3>🌐 ZeroTier</h3><div id=\"zt\">…</div>";
    const refresh = async () => {
      let s; try { s = await (await api("/api/zerotier")).json(); } catch (e) { return; }
      const nets = (s.networks || []).map(n => {
        const ip = (n.ip && n.ip !== "-") ? copyable(n.ip.split(",")[0]) : "—";
        const ok = n.status === "OK";
        return `<div class="r"><span>${n.nwid} ${ok ? "●" : "○"} ${n.status}</span><span>${ip} <button class="dbtn" data-leave="${n.nwid}" style="padding:1px 8px">×</button></span></div>`;
      }).join("") || `<div class="stub">${it ? "Nessuna rete." : "No networks."}</div>`;
      $("#zt", card).innerHTML =
        '<div class="rows"><div class="r"><span>' + (it ? "Nodo" : "Node") + "</span><span>" + copyable(s.address) + '</span></div><div class="r"><span>' + (it ? "Stato" : "Status") + "</span><span>" + (s.online ? "● ONLINE" : "○ offline") + "</span></div></div>" +
        '<div class="gl" style="margin-top:10px">' + (it ? "Reti" : "Networks") + '</div><div class="rows">' + nets + "</div>" +
        '<div class="brow" style="margin-top:8px"><input id="ztnw" class="dsel" placeholder="Network ID (16 hex)" style="flex:1"><button class="dbtn" id="ztj">' + (it ? "Entra" : "Join") + "</button></div>" +
        '<div class="stub" style="margin-top:8px">' + (it ? "Dopo «Entra», autorizza il nodo su my.zerotier.com. Poi raggiungi la dashboard da ovunque: https://&lt;IP ZeroTier&gt;:8443" : "After Join, authorize the node on my.zerotier.com. Then reach the dashboard from anywhere: https://&lt;ZeroTier IP&gt;:8443") + "</div>";
      card.querySelectorAll("[data-leave]").forEach(b => b.onclick = async () => { await action("/api/zerotier/leave", { nwid: b.dataset.leave }, it ? "Uscito dalla rete" : "Left network"); setTimeout(refresh, 800); });
      $("#ztj", card).onclick = async () => { await action("/api/zerotier/join", { nwid: $("#ztnw", card).value.trim() }, it ? "Richiesta inviata — autorizza su my.zerotier.com" : "Request sent — authorize on my.zerotier.com"); setTimeout(refresh, 1500); };
    };
    refresh(); card._iv = setInterval(refresh, 8000);
  },
  _stub(card, mod) { card.innerHTML = `<h3>${mod.icon} ${LANG === "it" ? mod.name : (mod.name_en || mod.name)}</h3><div class="stub">${LANG === "it" ? "Modulo attivo — interfaccia in arrivo." : "Module on — UI coming soon."}</div>`; },
};

async function buildDashboard() {
  $("#login").style.display = "none"; $("#app").style.display = "block";
  $("#logout").textContent = T("logout");
  let data; try { data = await (await api("/api/modules")).json(); } catch (e) { return showLogin(); }
  $("#host").textContent = data.host || "";
  const enabled = {}; (data.modules || []).forEach(m => enabled[m.id] = m);
  const grid = $("#grid"); grid.innerHTML = "";
  GROUPS.forEach(g => {
    const present = g.mods.filter(id => enabled[id]);
    if (!present.length) return;
    const h = document.createElement("div"); h.className = "grouphdr"; h.textContent = T(g.t); grid.appendChild(h);
    present.forEach(id => { const mod = enabled[id]; const card = document.createElement("div"); card.className = "mod";
      (RENDER[id] || ((c) => RENDER._stub(c, mod)))(card, mod); grid.appendChild(card); });
  });
  // session watcher: if the login session expires, drop back to the login screen
  clearInterval(window._sw);
  window._sw = setInterval(async () => { try { const r = await api("/api/me"); if (!r.ok) location.reload(); } catch (e) {} }, 60000);
}
function showLogin() {
  $("#app").style.display = "none"; $("#login").style.display = "grid";
  $("#lsub").textContent = T("login_sub"); $("#u").placeholder = T("user"); $("#p").placeholder = T("pass"); $("#lbtn").textContent = T("enter");
  $("#u").focus();
}
function setLang(l) { LANG = l; localStorage.setItem("sflang", l); location.reload(); }

$("#lform").addEventListener("submit", async ev => {
  ev.preventDefault(); $("#lerr").textContent = "";
  const r = await api("/api/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ user: $("#u").value, pass: $("#p").value }) });
  if (r.ok) { $("#p").value = ""; buildDashboard(); } else { const j = await r.json().catch(() => ({})); $("#lerr").textContent = j.error || T("denied"); }
});
$("#logout").addEventListener("click", async () => { await api("/api/logout", { method: "POST" }); location.reload(); });
$("#settings-btn").addEventListener("click", openSettings);
document.querySelectorAll(".lang-btn").forEach(b => b.addEventListener("click", () => setLang(b.dataset.l)));

(async () => {
  document.querySelectorAll(".lang-btn").forEach(b => b.classList.toggle("active", b.dataset.l === LANG));
  try { const r = await api("/api/me"); if (r.ok) buildDashboard(); else showLogin(); } catch (e) { showLogin(); }
})();
