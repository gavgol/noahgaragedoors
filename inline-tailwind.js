// Inlines the pre-built tailwind.css into every Tailwind page so first paint
// is always styled (no FOUC from a render-blocking CSS request).
// Idempotent: run it again after every tailwind.css rebuild.
//   node inline-tailwind.js
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const css = fs.readFileSync(path.join(ROOT, 'tailwind.css'), 'utf8').trim();

const PAGES = [
  'index.html',
  'gallery/index.html',
  'garage-door-springs/index.html',
  'garage-door-openers/index.html',
  'garage-door-off-track-repair/index.html',
  'garage-door-maintenance/index.html',
  'garage-door-cable-repair/index.html',
  'emergency-garage-door-repair/index.html',
  'new-garage-door/index.html',
];

const LINK_RE = /<link\s+rel="stylesheet"\s+href="\/tailwind\.css"\s*\/?>/;
const INLINE_RE = /<style data-tailwind-inline>[\s\S]*?<\/style>/;
const inlineBlock = () => `<style data-tailwind-inline>${css}</style>`;

let failed = false;
for (const page of PAGES) {
  const file = path.join(ROOT, page);
  const html = fs.readFileSync(file, 'utf8');
  let out;
  if (INLINE_RE.test(html)) {
    out = html.replace(INLINE_RE, inlineBlock);
  } else if (LINK_RE.test(html)) {
    out = html.replace(LINK_RE, inlineBlock);
  } else {
    console.error(`SKIP ${page}: no tailwind <link> or inline block found`);
    failed = true;
    continue;
  }
  fs.writeFileSync(file, out);
  console.log(`OK   ${page}`);
}
process.exit(failed ? 1 : 0);
