/** Tailwind v3 config for pre-building a static stylesheet (no runtime CDN).
 *  Build:  npx tailwindcss@3.4.19 -c tailwind.config.js -i tailwind-src/input.css -o tailwind.css --minify
 *  Only the pages that actually use Tailwind utility classes are scanned. */
module.exports = {
  content: [
    "./index.html",
    "./gallery/index.html",
    "./emergency-garage-door-repair/index.html",
    "./garage-door-cable-repair/index.html",
    "./garage-door-maintenance/index.html",
    "./garage-door-off-track-repair/index.html",
    "./garage-door-openers/index.html",
    "./garage-door-springs/index.html",
    "./new-garage-door/index.html",
  ],
  // Classes toggled at runtime by JS (not present often enough in static markup
  // to be reliably detected). Keep these so modals / lightbox / FAQ animations work.
  safelist: [
    "hidden", "flex", "rotate-180",
    "opacity-0", "opacity-100",
    "translate-y-0", "translate-y-10",
    "scale-95", "scale-100",
    "visible",
  ],
  theme: { extend: {} },
  plugins: [],
};
