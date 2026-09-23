/* Shared privacy controls and mobile contact actions. */
(function () {
  "use strict";

  var KEY = "ngd_cookie_consent";
  var PHONE = "6195724266";

  // Both floating bars below must get out of the way while the visitor is
  // actually looking at the #quote lead form, otherwise their high
  // z-index means they end up covering the submit button or last field.
  // Each bar registers a callback here; a single IntersectionObserver on
  // #quote (started once, from build()) drives all of them together.
  var quoteVisibilityCallbacks = [];
  // Last known state, so a bar that registers late (the consent banner is
  // now created after a short delay) starts in sync instead of waiting for
  // the next intersection change.
  var lastQuoteObscured = false;

  function onQuoteVisibilityChange(cb) {
    quoteVisibilityCallbacks.push(cb);
    if (lastQuoteObscured) cb(true);
  }

  // Inline icons (white, currentColor) for the mobile Call / Text bar.
  var ICON_PHONE =
    '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
    '<path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>';
  var ICON_TEXT =
    '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
    '<path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>';

  // Lets other widgets (the accessibility button) step aside while the
  // consent banner is on screen.
  function announceBanner(visible) {
    var root = document.documentElement;
    if (visible) root.setAttribute("data-ngd-cookie-banner", "shown");
    else root.removeAttribute("data-ngd-cookie-banner");
    window.dispatchEvent(new CustomEvent("ngd-cookie-banner", { detail: { visible: !!visible } }));
  }

  function initQuoteOverlapGuard() {
    if (!quoteVisibilityCallbacks.length) return;
    var quoteEl = document.getElementById("quote");
    // Pages without a #quote section (or older browsers without
    // IntersectionObserver) simply keep the bars' normal show/hide logic.
    if (!quoteEl || typeof IntersectionObserver === "undefined") return;
    var observer = new IntersectionObserver(
      function (entries) {
        for (var i = 0; i < entries.length; i++) {
          var obscuring = entries[i].isIntersecting;
          lastQuoteObscured = obscuring;
          for (var j = 0; j < quoteVisibilityCallbacks.length; j++) {
            quoteVisibilityCallbacks[j](obscuring);
          }
        }
      },
      { threshold: 0.2 }
    );
    observer.observe(quoteEl);
  }

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
      '<a href="tel:' + PHONE + '">' +
      '<span style="display:flex;line-height:1">' + ICON_PHONE + '</span>' +
      '<span>Call now</span></a>' +
      '<a href="sms:' + PHONE + '?&body=' +
      encodeURIComponent("Hi Noah, I need help with my garage door.") +
      '">' +
      '<span style="display:flex;line-height:1">' + ICON_TEXT + '</span>' +
      '<span>Text us</span></a>';
    bar.style.cssText =
      "position:fixed;left:12px;right:12px;bottom:12px;z-index:2147482000;" +
      "display:flex;gap:10px;padding:8px;background:rgba(10,15,30,.94);" +
      "border:1px solid rgba(255,255,255,.14);border-radius:18px;" +
      "box-shadow:0 10px 30px rgba(0,0,0,.4);" +
      "transition:transform .28s ease,opacity .28s ease;";
    Array.prototype.forEach.call(bar.querySelectorAll("a"), function (link) {
      link.style.cssText =
        "flex:1;padding:14px 10px;border-radius:13px;text-align:center;" +
        "display:flex;align-items:center;justify-content:center;gap:8px;" +
        "font:800 15.5px system-ui,sans-serif;letter-spacing:.2px;" +
        "text-decoration:none;color:white;" +
        "background:linear-gradient(135deg,#3b82f6,#1d4ed8);" +
        "box-shadow:0 6px 16px rgba(37,99,235,.45);" +
        "transition:transform .12s ease;-webkit-tap-highlight-color:transparent;";
      link.addEventListener("touchstart", function () {
        link.style.transform = "scale(.96)";
      }, { passive: true });
      link.addEventListener("touchend", function () {
        link.style.transform = "scale(1)";
      });
    });
    bar.lastChild.style.background = "linear-gradient(135deg,#14b8a6,#0d9488)";
    bar.lastChild.style.boxShadow = "0 6px 16px rgba(13,148,136,.45)";
    document.body.appendChild(bar);

    var media = window.matchMedia("(min-width: 768px)");
    // On the homepage the hero already shows Call/Quote buttons, so the bar
    // stays hidden until the visitor scrolls past the first screen.
    var isHome = location.pathname === "/" || /\/index\.html$/.test(location.pathname);
    // While the #quote lead form is in view, the bar would otherwise sit on
    // top of its submit button/last field, so it steps aside until the
    // visitor scrolls away from the form.
    var nearQuote = false;
    function sync() {
      bar.style.display = media.matches ? "none" : "flex";
      var show = (!isHome || window.scrollY > window.innerHeight * 0.8) && !nearQuote;
      bar.style.transform = show ? "translateY(0)" : "translateY(140%)";
      bar.style.opacity = show ? "1" : "0";
      bar.style.pointerEvents = show ? "auto" : "none";
    }
    sync();
    media.addEventListener("change", sync);
    window.addEventListener("scroll", sync, { passive: true });
    onQuoteVisibilityChange(function (obscured) {
      nearQuote = obscured;
      sync();
    });
  }

  // The banner no longer greets the visitor on load: it appears on the first
  // scroll or after 5 seconds, whichever comes first. Nothing optional loads
  // before a choice is made, so the delay does not change consent semantics.
  function scheduleConsentBanner() {
    if (savedChoice() || document.getElementById("ngd-cookie-banner")) return;
    var done = false;
    var timer = null;
    function go() {
      if (done) return;
      done = true;
      clearTimeout(timer);
      window.removeEventListener("scroll", go);
      addConsentBanner();
    }
    timer = setTimeout(go, 5000);
    window.addEventListener("scroll", go, { passive: true });
  }

  function addConsentBanner() {
    if (savedChoice() || document.getElementById("ngd-cookie-banner")) return;

    var mobile = window.matchMedia("(max-width: 639px)").matches;

    var bar = document.createElement("div");
    bar.id = "ngd-cookie-banner";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-live", "polite");
    bar.setAttribute("aria-label", "Cookie preferences");
    bar.style.cssText = mobile
      ? // Slim single row (~56px) that sits just above the Call/Text bar.
        "position:fixed;left:8px;right:8px;bottom:84px;z-index:2147483000;" +
        "background:rgba(17,17,24,.98);border:1px solid rgba(255,255,255,.12);border-radius:14px;" +
        "box-shadow:0 10px 30px rgba(0,0,0,.5);padding:8px 8px 8px 14px;color:#e6e6ec;" +
        "font:13px/1.3 system-ui,sans-serif;display:flex;flex-wrap:nowrap;align-items:center;gap:8px;" +
        "min-height:56px;box-sizing:border-box;transition:transform .28s ease,opacity .28s ease;"
      : "position:fixed;left:16px;right:16px;bottom:82px;z-index:2147483000;" +
        "max-width:680px;margin:0 auto;background:rgba(17,17,24,.98);" +
        "border:1px solid rgba(255,255,255,.12);border-radius:16px;" +
        "box-shadow:0 12px 40px rgba(0,0,0,.5);padding:18px 20px;color:#e6e6ec;" +
        "font:14px/1.55 system-ui,sans-serif;display:flex;flex-wrap:wrap;" +
        "align-items:center;gap:12px;transition:transform .28s ease,opacity .28s ease;";

    var text = document.createElement("div");
    text.style.cssText = mobile
      ? "flex:1 1 auto;min-width:0;color:rgba(255,255,255,.8);"
      : "flex:1 1 300px;color:rgba(255,255,255,.78);";
    text.innerHTML = mobile
      ? 'Optional analytics cookies. <a href="/privacy-policy.html" style="color:#60a5fa">Privacy</a>'
      : "Optional analytics help us understand which pages and ads lead to service requests. " +
        '<a href="/privacy-policy.html" style="color:#60a5fa">Privacy Policy</a>.';

    var decline = document.createElement("button");
    decline.type = "button";
    decline.textContent = "Decline";
    decline.style.cssText =
      "cursor:pointer;border:1px solid rgba(255,255,255,.25);background:transparent;" +
      "color:white;font-weight:700;border-radius:999px;flex-shrink:0;" +
      (mobile ? "padding:0 14px;height:40px;font-size:13px;" : "padding:10px 18px;");

    var accept = document.createElement("button");
    accept.type = "button";
    accept.textContent = mobile ? "Accept" : "Accept analytics";
    if (mobile) accept.setAttribute("aria-label", "Accept analytics");
    accept.style.cssText =
      "cursor:pointer;border:0;background:#2563eb;color:white;font-weight:700;" +
      "border-radius:999px;flex-shrink:0;" +
      (mobile ? "padding:0 16px;height:40px;font-size:13px;" : "padding:11px 20px;");

    function choose(choice) {
      saveChoice(choice);
      bar.remove();
      announceBanner(false);
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
    announceBanner(true);

    // Same idea as the contact bar: step out of the way while the visitor
    // is looking at the #quote form, so it can never cover the submit
    // button, then slide back once they scroll away (until dismissed).
    var nearQuote = false;
    function syncPosition() {
      var show = !nearQuote;
      bar.style.transform = show ? "translateY(0)" : "translateY(160%)";
      bar.style.opacity = show ? "1" : "0";
      bar.style.pointerEvents = show ? "auto" : "none";
    }
    onQuoteVisibilityChange(function (obscured) {
      nearQuote = obscured;
      syncPosition();
    });
  }

  function build() {
    if (savedChoice() === "accepted") loadAnalytics();
    addMobileContactBar();
    scheduleConsentBanner();
    initQuoteOverlapGuard();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
