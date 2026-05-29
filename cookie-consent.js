/* Noah Garage Doors — lightweight cookie consent notice (no dependencies).
   California/CCPA style: notice + dismiss, links to privacy policy.
   Remembers choice in localStorage so it shows once. */
(function () {
  "use strict";
  var KEY = "ngd_cookie_consent";
  try {
    if (localStorage.getItem(KEY) === "accepted") return;
  } catch (e) { /* localStorage blocked — show banner anyway */ }

  function build() {
    if (document.getElementById("ngd-cookie-banner")) return;

    var bar = document.createElement("div");
    bar.id = "ngd-cookie-banner";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-live", "polite");
    bar.setAttribute("aria-label", "Cookie notice");
    bar.style.cssText = [
      "position:fixed", "left:16px", "right:16px", "bottom:16px", "z-index:2147483000",
      "max-width:680px", "margin:0 auto",
      "background:rgba(17,17,24,0.97)", "backdrop-filter:blur(12px)",
      "-webkit-backdrop-filter:blur(12px)",
      "border:1px solid rgba(255,255,255,0.12)", "border-radius:16px",
      "box-shadow:0 12px 40px rgba(0,0,0,0.5)",
      "padding:18px 20px", "color:#e6e6ec",
      "font-family:'DM Sans',system-ui,-apple-system,Segoe UI,Roboto,sans-serif",
      "font-size:14px", "line-height:1.55",
      "display:flex", "flex-wrap:wrap", "align-items:center", "gap:14px",
      "transform:translateY(140%)", "transition:transform 0.45s cubic-bezier(0.16,1,0.3,1)"
    ].join(";");

    var text = document.createElement("div");
    text.style.cssText = "flex:1 1 300px;min-width:0;color:rgba(255,255,255,0.75);";
    text.innerHTML =
      "We use cookies and Google Analytics to understand site traffic and improve your experience. " +
      'By using this site, you agree to our use of cookies. <a href="/privacy-policy.html" ' +
      'style="color:#60a5fa;text-decoration:underline;white-space:nowrap;">Privacy Policy</a>.';

    var btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Got it";
    btn.style.cssText = [
      "flex:0 0 auto", "cursor:pointer", "border:0",
      "background:#2563EB", "color:#fff", "font-weight:700", "font-size:14px",
      "padding:11px 26px", "border-radius:999px", "white-space:nowrap",
      "box-shadow:0 0 18px rgba(37,99,235,0.45)", "transition:background 0.2s"
    ].join(";");
    btn.onmouseover = function () { btn.style.background = "#1D4ED8"; };
    btn.onmouseout = function () { btn.style.background = "#2563EB"; };

    function accept() {
      try { localStorage.setItem(KEY, "accepted"); } catch (e) {}
      bar.style.transform = "translateY(140%)";
      setTimeout(function () { if (bar.parentNode) bar.parentNode.removeChild(bar); }, 500);
    }
    btn.addEventListener("click", accept);

    bar.appendChild(text);
    bar.appendChild(btn);
    document.body.appendChild(bar);
    /* slide in */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { bar.style.transform = "translateY(0)"; });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
