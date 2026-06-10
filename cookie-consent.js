/* Shared privacy controls and mobile contact actions. */
(function () {
  "use strict";

  var KEY = "ngd_cookie_consent";
  var PHONE = "6195724266";

  function savedChoice() {
    try {
      return localStorage.getItem(KEY);
    } catch (error) {
      return null;
    }
  }

  function saveChoice(choice) {
    try {
      localStorage.setItem(KEY, choice);
    } catch (error) {
      // Privacy controls still work for the current page when storage is blocked.
    }
    window.dispatchEvent(
      new CustomEvent("ngd-consent", { detail: { analytics: choice === "accepted" } })
    );
    if (choice === "accepted") loadAnalytics();
  }

  function loadAnalytics() {
    if (window.ngdAnalyticsLoaded) return;
    window.ngdAnalyticsLoaded = true;

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () {
      window.dataLayer.push(arguments);
    };
    window.gtag("js", new Date());
    window.gtag("config", "G-HPY4V3C8T5");

    var google = document.createElement("script");
    google.async = true;
    google.src = "https://www.googletagmanager.com/gtag/js?id=G-HPY4V3C8T5";
    document.head.appendChild(google);

    window.fbq = function () {
      window.fbq.callMethod
        ? window.fbq.callMethod.apply(window.fbq, arguments)
        : window.fbq.queue.push(arguments);
    };
    window.fbq.queue = [];
    window.fbq.loaded = true;
    window.fbq.version = "2.0";
    var meta = document.createElement("script");
    meta.async = true;
    meta.src = "https://connect.facebook.net/en_US/fbevents.js";
    document.head.appendChild(meta);
    window.fbq("init", "1708916410247553");
    window.fbq("track", "PageView");
  }

  function addMobileContactBar() {
    if (document.getElementById("ngd-mobile-contact")) return;
    var bar = document.createElement("div");
    bar.id = "ngd-mobile-contact";
    bar.setAttribute("aria-label", "Contact Noah Garage Doors");
    bar.innerHTML =
      '<a href="tel:' + PHONE + '">Call now</a>' +
      '<a href="sms:' + PHONE + '?&body=' +
      encodeURIComponent("Hi Noah, I need help with my garage door.") +
      '">Text us</a>';
    bar.style.cssText =
      "position:fixed;left:12px;right:12px;bottom:12px;z-index:2147482000;" +
      "display:flex;gap:8px;padding:8px;background:rgba(10,15,30,.94);" +
      "border:1px solid rgba(255,255,255,.14);border-radius:16px;" +
      "box-shadow:0 10px 30px rgba(0,0,0,.4);";
    Array.prototype.forEach.call(bar.querySelectorAll("a"), function (link) {
      link.style.cssText =
        "flex:1;padding:12px 10px;border-radius:11px;text-align:center;" +
        "font:700 15px system-ui,sans-serif;text-decoration:none;color:white;" +
        "background:#2563eb;";
    });
    bar.lastChild.style.background = "#0f766e";
    document.body.appendChild(bar);

    var media = window.matchMedia("(min-width: 768px)");
    function sync() {
      bar.style.display = media.matches ? "none" : "flex";
    }
    sync();
    media.addEventListener("change", sync);
  }

  function addConsentBanner() {
    if (savedChoice() || document.getElementById("ngd-cookie-banner")) return;

    var bar = document.createElement("div");
    bar.id = "ngd-cookie-banner";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-live", "polite");
    bar.setAttribute("aria-label", "Cookie preferences");
    bar.style.cssText =
      "position:fixed;left:16px;right:16px;bottom:82px;z-index:2147483000;" +
      "max-width:680px;margin:0 auto;background:rgba(17,17,24,.98);" +
      "border:1px solid rgba(255,255,255,.12);border-radius:16px;" +
      "box-shadow:0 12px 40px rgba(0,0,0,.5);padding:18px 20px;color:#e6e6ec;" +
      "font:14px/1.55 system-ui,sans-serif;display:flex;flex-wrap:wrap;" +
      "align-items:center;gap:12px;";

    var text = document.createElement("div");
    text.style.cssText = "flex:1 1 300px;color:rgba(255,255,255,.78);";
    text.innerHTML =
      "Optional analytics help us understand which pages and ads lead to service requests. " +
      '<a href="/privacy-policy.html" style="color:#60a5fa">Privacy Policy</a>.';

    var decline = document.createElement("button");
    decline.type = "button";
    decline.textContent = "Decline";
    decline.style.cssText =
      "cursor:pointer;border:1px solid rgba(255,255,255,.25);background:transparent;" +
      "color:white;font-weight:700;padding:10px 18px;border-radius:999px;";

    var accept = document.createElement("button");
    accept.type = "button";
    accept.textContent = "Accept analytics";
    accept.style.cssText =
      "cursor:pointer;border:0;background:#2563eb;color:white;font-weight:700;" +
      "padding:11px 20px;border-radius:999px;";

    function choose(choice) {
      saveChoice(choice);
      bar.remove();
    }
    decline.addEventListener("click", function () {
      choose("declined");
    });
    accept.addEventListener("click", function () {
      choose("accepted");
    });

    bar.appendChild(text);
    bar.appendChild(decline);
    bar.appendChild(accept);
    document.body.appendChild(bar);
  }

  function build() {
    if (savedChoice() === "accepted") loadAnalytics();
    addMobileContactBar();
    addConsentBanner();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
