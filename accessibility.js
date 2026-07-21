/*
 * Noah Garage Doors — accessibility toolbar.
 *
 * This is deliberately NOT a third-party "compliance overlay". Those (accessiBe,
 * UserWay, etc.) claim to make a site WCAG-compliant automatically; the FTC fined
 * accessiBe $1M in 2025 for that false claim, and in 2025 ~23% of US website
 * accessibility lawsuits were filed against sites that HAD an overlay installed.
 * A widget does not create legal compliance and can increase risk.
 *
 * What this file actually is: a grouped set of honest, native controls the site's
 * OWN code applies (text size, spacing, contrast, links, cursor, motion, reading
 * guide, focus outline) plus a link to our real Accessibility Statement and a way
 * to report a barrier. It genuinely helps low-vision / dyslexic / motion-sensitive
 * / keyboard users and makes no compliance claim. The real protection is the
 * underlying site being accessible; this sits on top of that.
 *
 * Self-injecting (same pattern as cookie-consent.js) with inline styles so it is
 * immune to the prebuilt tailwind.css. Positioned to sit ABOVE the bottom Call/
 * Text bar on mobile and yields z-index to it, so it never hides the primary CTA.
 */
(function () {
  "use strict";
  if (window.__ngdA11yLoaded) return;
  window.__ngdA11yLoaded = true;

  var STORE_KEY = "ngd-a11y-v1";
  var ZOOM_STEPS = [1, 1.15, 1.3, 1.5];
  var ACCENT = "#2563EB";
  var FONT = "'DM Sans','Inter',system-ui,-apple-system,Segoe UI,sans-serif";

  var TOGGLES = [
    { key: "font",        group: "Reading",         label: "Readable font" },
    { key: "linespace",   group: "Reading",         label: "Line spacing" },
    { key: "letterspace", group: "Reading",         label: "Letter spacing" },
    { key: "contrast",    group: "Color & display", label: "High contrast" },
    { key: "links",       group: "Color & display", label: "Highlight links" },
    { key: "cursor",      group: "Color & display", label: "Big cursor" },
    { key: "motion",      group: "Motion & focus",  label: "Pause motion" },
    { key: "guide",       group: "Motion & focus",  label: "Reading guide" },
    { key: "focus",       group: "Motion & focus",  label: "Focus outline" }
  ];

  // ---- persisted state ------------------------------------------------------
  var state = { zoom: 0 };
  TOGGLES.forEach(function (t) { state[t.key] = false; });
  try {
    var saved = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
    for (var k in state) if (k in saved) state[k] = saved[k];
  } catch (e) {}
  function persist() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) {}
  }

  // ---- icons ----------------------------------------------------------------
  var I = {
    a11y: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" aria-hidden="true"><circle cx="12" cy="4" r="2" fill="currentColor"/><path d="M4 8c2.7 1.1 5.3 1.6 8 1.6S17.3 9.1 20 8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M12 9.4V15m0 0l-3 6M12 15l3 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    check: '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" aria-hidden="true"><path d="M5 12.5l4 4 10-10" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    minus: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true"><path d="M6 12h12" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    plus:  '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true"><path d="M12 6v12M6 12h12" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    reset: '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" aria-hidden="true"><path d="M4 5v5h5M4.5 10a8 8 0 113.4 8.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    help:  '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M9.6 9.4a2.4 2.4 0 114 1.8c-.9.7-1.6 1.2-1.6 2.3M12 16.6h.01" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    close: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    // control tile icons
    font:        '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><path d="M5 18L9.2 6h1.6L15 18M6.6 14h6.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M16.5 18l2.4-7h.2l2.4 7M17.4 15.6h4.2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    linespace:  '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><path d="M9 6h11M9 12h11M9 18h11" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M4 4v16M4 4L2.4 6M4 4l1.6 2M4 20l-1.6-2M4 20l1.6-2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    letterspace:'<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><path d="M12 4v16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" opacity=".5"/><path d="M3 12h5M21 12h-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M6 10l-2 2 2 2M18 10l2 2-2 2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    contrast:   '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M12 3a9 9 0 010 18z" fill="currentColor"/></svg>',
    links:      '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><path d="M9.5 14.5l5-5M8 13l-1.7 1.7a3.3 3.3 0 004.6 4.6L12.5 18M16 11l1.7-1.7a3.3 3.3 0 00-4.6-4.6L11.5 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    cursor:     '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><path d="M6 3l0 16 4-4 2.6 5.4 2.2-1L12 14h6z" fill="currentColor"/></svg>',
    motion:     '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><rect x="7" y="6" width="3.2" height="12" rx="1.2" fill="currentColor"/><rect x="13.8" y="6" width="3.2" height="12" rx="1.2" fill="currentColor"/></svg>',
    guide:      '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><path d="M3 7h18M3 17h18" stroke="currentColor" stroke-width="1.4" opacity=".5" stroke-linecap="round"/><rect x="3" y="10" width="18" height="4" rx="1.5" fill="currentColor"/></svg>',
    focus:      '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" aria-hidden="true"><path d="M4 8V6a2 2 0 012-2h2M20 8V6a2 2 0 00-2-2h-2M4 16v2a2 2 0 002 2h2M20 16v2a2 2 0 01-2 2h-2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="12" r="2.4" fill="currentColor"/></svg>'
  };

  // ---- CSS the controls toggle ---------------------------------------------
  var TXT = "html.CLS p, html.CLS li, html.CLS a, html.CLS span, html.CLS h1, html.CLS h2, html.CLS h3, html.CLS h4, html.CLS td, html.CLS label";
  var bigCursor = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='34' height='34' viewBox='0 0 34 34'%3E%3Cpath d='M6 3l0 22 5.5-5.5 3.4 7.2 3.6-1.7-3.4-7.1 7.4 0z' fill='%23000' stroke='%23fff' stroke-width='1.6'/%3E%3C/svg%3E\") 6 3, auto";
  var css = document.createElement("style");
  css.id = "ngd-a11y-css";
  css.textContent =
    // Scope high-contrast to the page BODY only. The widget (button, panel,
    // scrim, reading guide) is mounted on <html>, outside <body>, so it keeps its
    // own design and is never flattened — no per-element :not() exclusions, which
    // is what previously out-specified the panel's own background.
    "html.a11y-contrast { background:#000 !important; }" +
    "html.a11y-contrast body { background:#000 !important; color:#fff !important; }" +
    "html.a11y-contrast body * { background-color:transparent !important; color:#fff !important;" +
      " border-color:#fff !important; text-shadow:none !important; }" +
    "html.a11y-contrast body a { color:#ffde3d !important; }" +
    "html.a11y-contrast body img, html.a11y-contrast body video { filter:none !important; }" +
    "html.a11y-links a { text-decoration:underline !important; text-underline-offset:2px !important;" +
      " outline:1px dotted currentColor; outline-offset:2px; }" +
    TXT.replace(/CLS/g, "a11y-font") + "," + "html.a11y-font body {" +
      " font-family:Verdana, Tahoma, 'DejaVu Sans', Arial, sans-serif !important;" +
      " letter-spacing:0.01em !important; }" +
    TXT.replace(/CLS/g, "a11y-linespace") + " { line-height:2.05 !important; }" +
    "html.a11y-linespace p, html.a11y-linespace li { margin-bottom:1em !important; }" +
    TXT.replace(/CLS/g, "a11y-letterspace") + " { letter-spacing:0.12em !important; word-spacing:0.18em !important; }" +
    "html.a11y-cursor, html.a11y-cursor * { cursor:" + bigCursor + " !important; }" +
    "html.a11y-focus a:focus, html.a11y-focus button:focus, html.a11y-focus input:focus," +
    "html.a11y-focus select:focus, html.a11y-focus textarea:focus, html.a11y-focus [tabindex]:focus {" +
      " outline:3px solid #ffbf00 !important; outline-offset:3px !important; }" +
    "html.a11y-motion *, html.a11y-motion *::before, html.a11y-motion *::after {" +
      " animation:none !important; transition:none !important; scroll-behavior:auto !important; }" +
    "html.a11y-motion .reveal { opacity:1 !important; transform:none !important; }" +
    "#ngd-a11y-panel button:focus-visible, #ngd-a11y-btn:focus-visible {" +
      " outline:3px solid #8ab4ff !important; outline-offset:2px; }" +
    "#ngd-a11y-panel .a11y-tile:hover { border-color:rgba(255,255,255,.28); background:rgba(255,255,255,.07); }" +
    "#ngd-a11y-panel .a11y-tile.on:hover { border-color:" + ACCENT + "; }" +
    "#ngd-a11y-panel .a11y-step:not(:disabled):hover { background:rgba(255,255,255,.14); }" +
    "#ngd-a11y-panel::-webkit-scrollbar { width:10px; }" +
    "#ngd-a11y-panel::-webkit-scrollbar-thumb { background:rgba(255,255,255,.14); border-radius:99px; border:3px solid #0e1424; }";
  (document.head || document.documentElement).appendChild(css);

  // ---- reading guide (JS-driven ruler) -------------------------------------
  var guideEl = null;
  function moveGuide(e) {
    var y = e.touches && e.touches[0] ? e.touches[0].clientY : e.clientY;
    if (guideEl && y != null) guideEl.style.top = y + "px";
  }
  function setGuide(on) {
    if (on) {
      if (!guideEl) {
        guideEl = document.createElement("div");
        guideEl.id = "ngd-a11y-guide";
        guideEl.style.cssText =
          "position:fixed;left:0;right:0;top:50%;height:46px;z-index:2147481500;pointer-events:none;" +
          "transform:translateY(-50%);background:rgba(37,99,235,.12);" +
          "border-top:2px solid rgba(37,99,235,.75);border-bottom:2px solid rgba(37,99,235,.75);";
        // Mounted on <html>, not <body>, so the body `zoom` control never scales it.
        document.documentElement.appendChild(guideEl);
        window.addEventListener("pointermove", moveGuide, { passive: true });
        window.addEventListener("touchmove", moveGuide, { passive: true });
      }
      guideEl.style.display = "block";
    } else if (guideEl) {
      guideEl.style.display = "none";
    }
  }

  function apply() {
    var h = document.documentElement;
    TOGGLES.forEach(function (t) {
      if (t.key === "guide") return;
      h.classList.toggle("a11y-" + t.key, !!state[t.key]);
    });
    setGuide(!!state.guide);
    var z = ZOOM_STEPS[state.zoom] || 1;
    document.body.style.zoom = z === 1 ? "" : String(z);
    sync();
  }

  // ---- launcher button ------------------------------------------------------
  var btn = document.createElement("button");
  btn.id = "ngd-a11y-btn";
  btn.type = "button";
  btn.setAttribute("aria-haspopup", "dialog");
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-label", "Accessibility options");
  btn.innerHTML = '<span style="color:#fff;display:flex">' + I.a11y + "</span>";
  btn.style.cssText =
    "position:fixed;left:18px;bottom:96px;z-index:2147481000;" +
    "width:54px;height:54px;border-radius:50%;border:0;cursor:pointer;padding:0;" +
    "display:flex;align-items:center;justify-content:center;" +
    "background:linear-gradient(145deg,#3b82f6,#1d4ed8);" +
    "box-shadow:0 8px 22px rgba(37,99,235,.5),inset 0 1px 0 rgba(255,255,255,.35);" +
    "transition:transform .15s ease,opacity .25s ease;-webkit-tap-highlight-color:transparent;";
  btn.addEventListener("mouseenter", function () { if (revealed) btn.style.transform = "scale(1.07)"; });
  btn.addEventListener("mouseleave", function () { if (revealed) btn.style.transform = "scale(1)"; });

  var desk = window.matchMedia("(min-width:768px)");
  function placeButton() {
    btn.style.bottom = desk.matches ? "24px" : "96px";
    if (isOpen) positionPanel();
  }

  var isHome = location.pathname === "/" || /\/index\.html$/.test(location.pathname);
  var revealed = !isHome;
  function setShown(show) {
    btn.style.opacity = show ? "1" : "0";
    btn.style.transform = show ? "scale(1)" : "scale(.6)";
    btn.style.pointerEvents = show ? "auto" : "none";
  }
  function revealNow() { if (!revealed) { revealed = true; setShown(true); } }
  function onScrollReveal() { if (window.scrollY > window.innerHeight * 0.8) revealNow(); }

  // ---- scrim ----------------------------------------------------------------
  var scrim = document.createElement("div");
  scrim.id = "ngd-a11y-scrim";
  scrim.hidden = true;
  scrim.style.cssText =
    "position:fixed;inset:0;z-index:2147483400;background:rgba(3,7,18,.5);" +
    "opacity:0;transition:opacity .18s ease;backdrop-filter:blur(2px);";
  scrim.addEventListener("click", close);

  // ---- panel ----------------------------------------------------------------
  var panel = document.createElement("div");
  panel.id = "ngd-a11y-panel";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "Accessibility options");
  panel.hidden = true;
  panel.style.cssText =
    "position:fixed;left:18px;z-index:2147483500;width:326px;max-width:calc(100vw - 32px);" +
    "max-height:min(80vh,600px);overflow-y:auto;padding:0;border-radius:22px;" +
    "background:#0e1424;border:1px solid rgba(255,255,255,.10);color:#f3f5f9;" +
    "box-shadow:0 24px 70px rgba(0,0,0,.6);font-family:" + FONT + ";-webkit-font-smoothing:antialiased;";

  // header
  var header = document.createElement("div");
  header.style.cssText =
    "position:sticky;top:0;z-index:2;display:flex;align-items:center;gap:12px;padding:17px 18px 14px;" +
    "background:linear-gradient(180deg,#14203a,#0e1424);border-bottom:1px solid rgba(255,255,255,.07);";
  header.innerHTML =
    '<span style="flex:0 0 auto;width:40px;height:40px;border-radius:12px;display:flex;align-items:center;' +
    'justify-content:center;color:#fff;background:linear-gradient(145deg,#3b82f6,#1d4ed8);box-shadow:0 4px 12px rgba(37,99,235,.45)">' + I.a11y + "</span>" +
    '<span style="flex:1 1 auto;min-width:0">' +
      '<span style="display:block;font-weight:700;font-size:16px;letter-spacing:-.01em">Accessibility</span>' +
      '<span style="display:block;font-size:12.5px;color:rgba(255,255,255,.55);margin-top:1px">Adjust this site to suit you</span>' +
    "</span>";
  var closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.setAttribute("aria-label", "Close accessibility options");
  closeBtn.innerHTML = I.close;
  closeBtn.style.cssText =
    "flex:0 0 auto;width:34px;height:34px;border-radius:10px;border:1px solid rgba(255,255,255,.12);" +
    "background:rgba(255,255,255,.05);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;";
  closeBtn.addEventListener("click", close);
  header.appendChild(closeBtn);
  panel.appendChild(header);

  var bodyEl = document.createElement("div");
  bodyEl.style.cssText = "padding:16px 18px 6px;";
  panel.appendChild(bodyEl);

  // text-size stepper
  var sizeWrap = document.createElement("div");
  sizeWrap.style.cssText =
    "border:1px solid rgba(255,255,255,.10);border-radius:16px;padding:13px 14px;margin-bottom:16px;background:rgba(255,255,255,.035);";
  sizeWrap.innerHTML =
    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:11px">' +
      '<span style="font-weight:650;font-size:14.5px">Text size</span>' +
      '<span id="ngd-a11y-zoomval" aria-live="polite" style="font-weight:700;font-size:13px;color:#9cc0ff">100%</span>' +
    "</div>";
  var sizeRow = document.createElement("div");
  sizeRow.style.cssText = "display:flex;align-items:center;gap:12px;";
  var minusBtn = stepBtn(I.minus, "Decrease text size", -1);
  var plusBtn = stepBtn(I.plus, "Increase text size", 1);
  var meter = document.createElement("div");
  meter.setAttribute("aria-hidden", "true");
  meter.style.cssText = "flex:1 1 auto;display:flex;gap:5px;";
  for (var m = 0; m < ZOOM_STEPS.length; m++) {
    var seg = document.createElement("span");
    seg.style.cssText = "flex:1;height:7px;border-radius:99px;background:rgba(255,255,255,.12);transition:background .15s ease;";
    meter.appendChild(seg);
  }
  sizeRow.appendChild(minusBtn);
  sizeRow.appendChild(meter);
  sizeRow.appendChild(plusBtn);
  sizeWrap.appendChild(sizeRow);
  bodyEl.appendChild(sizeWrap);

  function stepBtn(icon, label, dir) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "a11y-step";
    b.setAttribute("aria-label", label); b.innerHTML = icon;
    b.style.cssText =
      "flex:0 0 auto;width:38px;height:38px;border-radius:11px;cursor:pointer;color:#fff;display:flex;" +
      "align-items:center;justify-content:center;background:rgba(255,255,255,.08);" +
      "border:1px solid rgba(255,255,255,.14);transition:background .12s ease;";
    b.addEventListener("click", function () {
      var next = state.zoom + dir;
      if (next < 0 || next >= ZOOM_STEPS.length) return;
      state.zoom = next; persist(); apply();
    });
    return b;
  }

  // grouped toggle tiles
  var tileEls = {};
  var groupsSeen = [];
  TOGGLES.forEach(function (t) {
    var g = t.group;
    if (groupsSeen.indexOf(g) === -1) {
      groupsSeen.push(g);
      var lbl = document.createElement("div");
      lbl.textContent = g;
      lbl.style.cssText =
        "font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;" +
        "color:rgba(255,255,255,.42);margin:6px 2px 9px;";
      bodyEl.appendChild(lbl);
      var grid = document.createElement("div");
      grid.dataset.group = g;
      grid.style.cssText = "display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;";
      bodyEl.appendChild(grid);
    }
    var container = bodyEl.querySelector('[data-group="' + g + '"]');
    var b = document.createElement("button");
    b.type = "button"; b.className = "a11y-tile"; b.dataset.key = t.key;
    b.setAttribute("aria-pressed", "false"); b.setAttribute("aria-label", t.label);
    b.style.cssText =
      "position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:8px;" +
      "padding:13px 12px;border-radius:15px;cursor:pointer;text-align:left;min-height:90px;" +
      "background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.10);color:#e7ecf5;" +
      "font-family:" + FONT + ";transition:background .14s ease,border-color .14s ease,color .14s ease;";
    b.innerHTML =
      '<span class="a11y-ic" style="display:flex;color:rgba(255,255,255,.75);transition:color .14s ease">' + I[t.key] + "</span>" +
      '<span style="font-weight:650;font-size:13px;line-height:1.2">' + t.label + "</span>" +
      '<span class="a11y-chk" aria-hidden="true" style="position:absolute;top:10px;right:10px;width:19px;height:19px;' +
      'border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;background:' + ACCENT +
      ';opacity:0;transform:scale(.6);transition:opacity .14s ease,transform .14s ease">' + I.check + "</span>";
    b.addEventListener("click", function () {
      state[t.key] = !state[t.key]; persist(); apply();
    });
    tileEls[t.key] = b;
    container.appendChild(b);
  });

  // footer: reset + help
  var foot = document.createElement("div");
  foot.style.cssText = "padding:6px 18px 16px;";
  var reset = document.createElement("button");
  reset.type = "button";
  reset.innerHTML = '<span style="display:flex;color:rgba(255,255,255,.6)">' + I.reset + "</span><span>Reset all</span>";
  reset.style.cssText =
    "width:100%;display:flex;align-items:center;justify-content:center;gap:8px;margin:4px 0 12px;padding:11px;" +
    "border-radius:12px;cursor:pointer;font:650 13.5px " + FONT + ";color:rgba(255,255,255,.82);" +
    "background:transparent;border:1px solid rgba(255,255,255,.14);transition:background .12s ease;";
  reset.addEventListener("mouseenter", function () { reset.style.background = "rgba(255,255,255,.06)"; });
  reset.addEventListener("mouseleave", function () { reset.style.background = "transparent"; });
  reset.addEventListener("click", function () {
    state = { zoom: 0 };
    TOGGLES.forEach(function (t) { state[t.key] = false; });
    persist(); apply();
  });
  foot.appendChild(reset);
  var help = document.createElement("div");
  help.style.cssText =
    "display:flex;align-items:flex-start;gap:8px;font-size:12.5px;line-height:1.55;color:rgba(255,255,255,.6);" +
    "border-top:1px solid rgba(255,255,255,.08);padding-top:13px;";
  help.innerHTML =
    '<span style="flex:0 0 auto;color:rgba(255,255,255,.45);margin-top:1px">' + I.help + "</span>" +
    '<span>Something hard to use? Read our ' +
    '<a href="/accessibility.html" style="color:#9cc0ff;text-decoration:underline">Accessibility Statement</a>' +
    ' or call <a href="tel:6195724266" style="color:#9cc0ff;text-decoration:underline;white-space:nowrap">(619) 572-4266</a>.</span>';
  foot.appendChild(help);
  panel.appendChild(foot);

  // ---- reflect state into UI -----------------------------------------------
  function sync() {
    var lvl = state.zoom;
    document.getElementById("ngd-a11y-zoomval").textContent = Math.round(ZOOM_STEPS[lvl] * 100) + "%";
    Array.prototype.forEach.call(meter.children, function (seg, idx) {
      seg.style.background = idx <= lvl && lvl > 0 ? ACCENT : "rgba(255,255,255,.12)";
    });
    minusBtn.disabled = lvl === 0;
    plusBtn.disabled = lvl === ZOOM_STEPS.length - 1;
    [minusBtn, plusBtn].forEach(function (b) {
      b.style.opacity = b.disabled ? ".38" : "1";
      b.style.cursor = b.disabled ? "default" : "pointer";
    });
    TOGGLES.forEach(function (t) {
      var el = tileEls[t.key], on = !!state[t.key];
      el.classList.toggle("on", on);
      el.setAttribute("aria-pressed", on ? "true" : "false");
      el.style.background = on ? "rgba(37,99,235,.16)" : "rgba(255,255,255,.045)";
      el.style.borderColor = on ? ACCENT : "rgba(255,255,255,.10)";
      el.style.color = on ? "#fff" : "#e7ecf5";
      el.querySelector(".a11y-ic").style.color = on ? "#9cc0ff" : "rgba(255,255,255,.75)";
      var chk = el.querySelector(".a11y-chk");
      chk.style.opacity = on ? "1" : "0";
      chk.style.transform = on ? "scale(1)" : "scale(.6)";
    });
  }

  // ---- position / open / close ---------------------------------------------
  function positionPanel() { panel.style.bottom = (desk.matches ? 88 : 160) + "px"; }
  var isOpen = false;
  function open() {
    if (isOpen) return;
    isOpen = true;
    scrim.hidden = false; panel.hidden = false;
    positionPanel();
    void scrim.offsetWidth; scrim.style.opacity = "1";
    panel.scrollTop = 0;
    btn.setAttribute("aria-expanded", "true");
    var first = panel.querySelector("button.a11y-step:not([disabled]), button.a11y-tile");
    if (first) first.focus();
    document.addEventListener("keydown", onKey, true);
  }
  function close() {
    if (!isOpen) return;
    isOpen = false;
    panel.hidden = true;
    scrim.style.opacity = "0";
    setTimeout(function () { if (!isOpen) scrim.hidden = true; }, 200);
    btn.setAttribute("aria-expanded", "false");
    document.removeEventListener("keydown", onKey, true);
    btn.focus();
  }
  function onKey(e) { if (e.key === "Escape") { e.preventDefault(); close(); } }
  btn.addEventListener("click", function () { isOpen ? close() : open(); });

  // ---- mount ----------------------------------------------------------------
  function mount() {
    // Mount the widget on <html>, NOT <body>: the "Bigger text" control sets
    // `document.body.style.zoom`, which would otherwise scale the panel/button
    // too and push the panel off-screen. As children of <html> they stay at true
    // viewport scale while only the page content zooms.
    var root = document.documentElement;
    root.appendChild(scrim);
    root.appendChild(btn);
    root.appendChild(panel);
    placeButton();
    desk.addEventListener("change", placeButton);
    if (isHome) {
      setShown(false);
      window.addEventListener("scroll", onScrollReveal, { passive: true });
      btn.addEventListener("focus", revealNow);
    } else { setShown(true); }
    apply();
  }
  if (document.body) mount();
  else document.addEventListener("DOMContentLoaded", mount);
})();
