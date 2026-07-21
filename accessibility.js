/*
 * Noah Garage Doors — accessibility toolbar.
 *
 * This is deliberately NOT a third-party "compliance overlay". Those (accessiBe,
 * UserWay, etc.) claim to make a site WCAG-compliant automatically; the FTC fined
 * accessiBe $1M in 2025 for that false claim, and in 2025 ~23% of US website
 * accessibility lawsuits were filed against sites that HAD an overlay installed.
 * A widget does not create legal compliance and can increase risk.
 *
 * What this file actually is: a small set of honest, native controls the site's
 * OWN code applies (zoom, high contrast, readable font, highlight links, pause
 * motion) plus a link to our real Accessibility Statement and a way to report a
 * barrier. It genuinely helps low-vision / motion-sensitive / keyboard users and
 * makes no compliance claim. The real protection is the underlying site being
 * accessible; this sits on top of that.
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
  var BRAND = "#2563EB";

  // ---- persisted state ------------------------------------------------------
  var state = { zoom: 0, contrast: false, links: false, font: false, motion: false };
  try {
    var saved = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
    for (var k in state) if (k in saved) state[k] = saved[k];
  } catch (e) {}

  function persist() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) {}
  }

  // ---- the CSS the controls toggle -----------------------------------------
  var css = document.createElement("style");
  css.id = "ngd-a11y-css";
  css.textContent =
    "html.a11y-contrast, html.a11y-contrast body { background:#000 !important; color:#fff !important; }" +
    "html.a11y-contrast a { color:#ffde3d !important; }" +
    "html.a11y-contrast *:not(#ngd-a11y-btn):not(#ngd-a11y-btn *) {" +
      " background-color:transparent !important; color:#fff !important;" +
      " border-color:#fff !important; text-shadow:none !important; }" +
    "html.a11y-contrast img, html.a11y-contrast video { filter:none !important; }" +
    // The widget's own panel must NOT be flattened by the contrast override above
    // (that is what made it look transparent). Re-assert its surface with id
    // specificity so it stays a solid, readable menu in every mode.
    "html.a11y-contrast #ngd-a11y-panel { background:#0d1220 !important; border:1px solid #fff !important; }" +
    "html.a11y-contrast #ngd-a11y-panel button { background:rgba(255,255,255,.12) !important; border:1px solid #fff !important; }" +
    "html.a11y-contrast #ngd-a11y-panel .a11y-ind { border:1px solid #fff !important; }" +
    "html.a11y-contrast #ngd-a11y-scrim { background:rgba(0,0,0,.6) !important; }" +
    "html.a11y-links a { text-decoration:underline !important; text-underline-offset:2px !important;" +
      " outline:1px dotted currentColor; outline-offset:2px; }" +
    "html.a11y-font, html.a11y-font body," +
    "html.a11y-font p, html.a11y-font li, html.a11y-font a, html.a11y-font span," +
    "html.a11y-font h1, html.a11y-font h2, html.a11y-font h3, html.a11y-font h4," +
    "html.a11y-font button, html.a11y-font input, html.a11y-font label, html.a11y-font td {" +
      " font-family:Verdana, Tahoma, 'DejaVu Sans', Arial, sans-serif !important;" +
      " letter-spacing:0.02em !important; word-spacing:0.08em !important; line-height:1.7 !important; }" +
    "html.a11y-motion *, html.a11y-motion *::before, html.a11y-motion *::after {" +
      " animation:none !important; transition:none !important; scroll-behavior:auto !important; }" +
    // reveal-on-scroll elements must not stay invisible once motion is paused
    "html.a11y-motion .reveal { opacity:1 !important; transform:none !important; }";
  (document.head || document.documentElement).appendChild(css);

  function apply() {
    var h = document.documentElement;
    h.classList.toggle("a11y-contrast", !!state.contrast);
    h.classList.toggle("a11y-links", !!state.links);
    h.classList.toggle("a11y-font", !!state.font);
    h.classList.toggle("a11y-motion", !!state.motion);
    // Zoom genuinely enlarges content for low-vision users. `zoom` is supported
    // in all current major browsers and, unlike a transform, keeps layout flow.
    var z = ZOOM_STEPS[state.zoom] || 1;
    document.body.style.zoom = z === 1 ? "" : String(z);
    syncButtons();
  }

  // ---- build the launcher button -------------------------------------------
  var btn = document.createElement("button");
  btn.id = "ngd-a11y-btn";
  btn.type = "button";
  btn.setAttribute("aria-haspopup", "dialog");
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-label", "Accessibility options");
  btn.innerHTML =
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false">' +
    '<circle cx="12" cy="3.5" r="2.1" fill="#fff"/>' +
    '<path d="M3 7.5c2.8 1.2 5.7 1.8 9 1.8s6.2-.6 9-1.8" stroke="#fff" stroke-width="1.9" stroke-linecap="round"/>' +
    '<path d="M12 8.8V15m0 0l-3.2 5.4M12 15l3.2 5.4" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>' +
    "</svg>";
  // z-index sits BELOW the Call/Text bar (2147482000) and cookie banner
  // (2147483000) so it can never cover the primary CTA. It is positioned above
  // the bar anyway, so in practice they don't overlap.
  btn.style.cssText =
    "position:fixed;left:16px;bottom:96px;z-index:2147481000;" +
    "width:52px;height:52px;border-radius:50%;border:2px solid rgba(255,255,255,.85);" +
    "background:" + BRAND + ";color:#fff;cursor:pointer;display:flex;" +
    "align-items:center;justify-content:center;padding:0;" +
    "box-shadow:0 6px 20px rgba(37,99,235,.5);transition:transform .15s ease,opacity .25s ease;" +
    "-webkit-tap-highlight-color:transparent;";
  btn.addEventListener("mouseenter", function () { btn.style.transform = "scale(1.06)"; });
  btn.addEventListener("mouseleave", function () { btn.style.transform = "scale(1)"; });

  // On desktop the mobile Call/Text bar is hidden, so drop the button to the
  // normal corner. A media listener keeps it correct on resize/rotate.
  var desk = window.matchMedia("(min-width:768px)");
  function placeButton() { btn.style.bottom = desk.matches ? "24px" : "96px"; }
  placeButton();
  desk.addEventListener("change", placeButton);

  // On the homepage the hero already carries the main CTAs, so — like the Call/
  // Text bar — the launcher stays hidden until the visitor scrolls past the first
  // screen. It still reveals on keyboard focus so Tab users always reach it, and
  // it stays in the DOM the whole time. On every other page it shows immediately.
  var isHome = location.pathname === "/" || /\/index\.html$/.test(location.pathname);
  var revealed = !isHome;
  function setShown(show) {
    btn.style.opacity = show ? "1" : "0";
    btn.style.transform = show ? "scale(1)" : "scale(.6)";
    btn.style.pointerEvents = show ? "auto" : "none";
  }
  function revealNow() { if (!revealed) { revealed = true; setShown(true); } }
  function onScrollReveal() { if (window.scrollY > window.innerHeight * 0.8) revealNow(); }
  if (isHome) {
    setShown(false);
    window.addEventListener("scroll", onScrollReveal, { passive: true });
    btn.addEventListener("focus", revealNow);
  } else {
    setShown(true);
  }

  // ---- dim scrim behind the open panel (makes it read as a clean menu) ------
  var scrim = document.createElement("div");
  scrim.id = "ngd-a11y-scrim";
  scrim.hidden = true;
  scrim.style.cssText =
    "position:fixed;inset:0;z-index:2147483400;background:rgba(0,0,0,.45);" +
    "opacity:0;transition:opacity .18s ease;";
  scrim.addEventListener("click", close);

  // ---- build the panel ------------------------------------------------------
  var panel = document.createElement("div");
  panel.id = "ngd-a11y-panel";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-modal", "false");
  panel.setAttribute("aria-label", "Accessibility options");
  panel.hidden = true;
  panel.style.cssText =
    "position:fixed;left:16px;bottom:160px;z-index:2147483500;width:290px;max-width:calc(100vw - 32px);" +
    "max-height:min(70vh,520px);overflow-y:auto;padding:16px;border-radius:18px;" +
    "background:#0d1220;border:1px solid rgba(255,255,255,.16);" +
    "box-shadow:0 18px 50px rgba(0,0,0,.55);font-family:system-ui,-apple-system,Segoe UI,sans-serif;" +
    "color:#fff;";

  var controls = [
    { key: "zoom", label: "Bigger text", type: "cycle" },
    { key: "contrast", label: "High contrast", type: "toggle" },
    { key: "links", label: "Highlight links", type: "toggle" },
    { key: "font", label: "Readable font", type: "toggle" },
    { key: "motion", label: "Pause animations", type: "toggle" }
  ];

  var head = document.createElement("div");
  head.style.cssText = "display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;";
  head.innerHTML = '<strong style="font-size:15px;letter-spacing:.2px;">Accessibility</strong>';
  var closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.setAttribute("aria-label", "Close accessibility options");
  closeBtn.textContent = "×";
  closeBtn.style.cssText =
    "background:none;border:none;color:#fff;font-size:26px;line-height:1;cursor:pointer;padding:0 4px;";
  closeBtn.addEventListener("click", close);
  head.appendChild(closeBtn);
  panel.appendChild(head);

  var buttonEls = {};
  controls.forEach(function (c) {
    var b = document.createElement("button");
    b.type = "button";
    b.dataset.key = c.key;
    b.style.cssText =
      "display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;" +
      "margin-bottom:8px;padding:12px 14px;border-radius:12px;cursor:pointer;text-align:left;" +
      "font:600 14.5px system-ui,sans-serif;color:#fff;" +
      "background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);" +
      "transition:background .12s ease,border-color .12s ease;";
    b.innerHTML = '<span>' + c.label + '</span><span class="a11y-ind" aria-hidden="true"></span>';
    b.addEventListener("click", function () {
      if (c.type === "cycle") {
        state.zoom = (state.zoom + 1) % ZOOM_STEPS.length;
      } else {
        state[c.key] = !state[c.key];
      }
      persist();
      apply();
    });
    buttonEls[c.key] = b;
    panel.appendChild(b);
  });

  var reset = document.createElement("button");
  reset.type = "button";
  reset.textContent = "Reset all";
  reset.style.cssText =
    "width:100%;margin:4px 0 12px;padding:11px;border-radius:12px;cursor:pointer;" +
    "font:700 14px system-ui,sans-serif;color:#fff;background:rgba(239,68,68,.16);" +
    "border:1px solid rgba(239,68,68,.4);";
  reset.addEventListener("click", function () {
    state = { zoom: 0, contrast: false, links: false, font: false, motion: false };
    persist();
    apply();
  });
  panel.appendChild(reset);

  var foot = document.createElement("div");
  foot.style.cssText = "font-size:12.5px;line-height:1.55;color:rgba(255,255,255,.62);border-top:1px solid rgba(255,255,255,.1);padding-top:12px;";
  foot.innerHTML =
    'Trouble using this site? ' +
    '<a href="/accessibility.html" style="color:#7cb0ff;text-decoration:underline;">Accessibility Statement</a>' +
    ' or call <a href="tel:6195724266" style="color:#7cb0ff;text-decoration:underline;white-space:nowrap;">(619) 572-4266</a>.';
  panel.appendChild(foot);

  function syncButtons() {
    controls.forEach(function (c) {
      var el = buttonEls[c.key];
      var ind = el.querySelector(".a11y-ind");
      var on;
      if (c.type === "cycle") {
        on = state.zoom > 0;
        ind.textContent = on ? Math.round(ZOOM_STEPS[state.zoom] * 100) + "%" : "Off";
      } else {
        on = !!state[c.key];
        ind.textContent = on ? "On" : "Off";
      }
      el.setAttribute("aria-pressed", on ? "true" : "false");
      ind.style.cssText = "font-weight:700;font-size:12.5px;padding:2px 8px;border-radius:999px;" +
        (on ? "background:" + BRAND + ";color:#fff;" : "background:rgba(255,255,255,.1);color:rgba(255,255,255,.6);");
      el.style.borderColor = on ? "rgba(37,99,235,.6)" : "rgba(255,255,255,.12)";
    });
  }

  // ---- open / close ---------------------------------------------------------
  var isOpen = false;
  function open() {
    if (isOpen) return;
    isOpen = true;
    scrim.hidden = false;
    panel.hidden = false;
    panel.style.bottom = (desk.matches ? 88 : 160) + "px";
    void scrim.offsetWidth; // force reflow so the fade-in runs
    scrim.style.opacity = "1";
    btn.setAttribute("aria-expanded", "true");
    var first = panel.querySelector("button[data-key]");
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
    document.body.appendChild(scrim);
    document.body.appendChild(btn);
    document.body.appendChild(panel);
    apply(); // re-apply any saved preferences on every page load
  }
  if (document.body) mount();
  else document.addEventListener("DOMContentLoaded", mount);
})();
