import { readFile, writeFile, mkdir, rm, cp } from 'node:fs/promises';
import { resolve } from 'node:path';
import MarkdownIt from 'markdown-it';

const out = resolve('dist');
const catalog = JSON.parse(await readFile('content/public/catalog.json', 'utf8'));
const maps = JSON.parse(await readFile('content/public/maps.json', 'utf8'));
const lexicon = JSON.parse(await readFile('content/public/lexicon.json', 'utf8'));
const esc = value => String(value).replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[c]);
const md = new MarkdownIt({ html: false, linkify: false, typographer: false });
const renderLink = md.renderer.rules.link_open || ((tokens, i, options, env, self) => self.renderToken(tokens, i, options));
md.renderer.rules.link_open = (tokens, i, options, env, self) => {
  const href = tokens[i].attrGet('href');
  if (href && !/^[a-z]+:/i.test(href)) tokens[i].attrSet('href', href.replace(/^([a-z-]+)\.md(?=#|$)/, '$1.html').replace(/^\.\.\/\.\.\/assets\//, 'assets/'));
  return renderLink(tokens, i, options, env, self);
};
const slug = value => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section';
const sections = [
  ['worlds', 'Worlds', 'The two worlds', 'The landscapes, climates and deep histories of Erde and Dverghamar.'],
  ['peoples', 'Peoples', 'Peoples and natural history', 'Native lineages, divergent adaptations and the communities that connect them.'],
  ['cosmology', 'Cosmology', 'The Otherworld and magic', 'The Otherworld, living spirits, souls and the limits of coherent reality.'],
  ['language', 'Language', 'The speech of the Hamarkorar', 'Korvar, five regional traditions, and a vocabulary rooted in stone and everyday life.'],
  ['maps', 'Maps', 'The atlas', 'Thirteen maps explain planetary geometry, habitats and settlement systems.']
];
const pageTitles = Object.fromEntries(sections.map(([id, name]) => [id, name]));
for (const map of maps) {
  const svg = await readFile(`assets/maps/${map.stem}.svg`, 'utf8');
  const viewBox = svg.match(/viewBox="([^"]+)"/);
  if (!viewBox) throw new Error(`Missing map viewBox: ${map.stem}`);
  const [, , width, height] = viewBox[1].trim().split(/\s+/).map(Number);
  map.width = width; map.height = height;
}
const searchIndex = [];
const logo = '<svg viewBox="0 0 32 36" width="28" height="32" fill="none" aria-hidden="true"><path d="M16 2 30 10v16L16 34 2 26V10Z" stroke="currentColor" stroke-width="1.5"/><path d="m7 24 9-15 9 15M11 18h10M16 9v22" stroke="currentColor" stroke-width="1.5"/></svg>';
function layout(title, active, body, { toc = '', description = '', file = '' } = {}) {
  const nav = sections.map(([id, name], i) => `<a href="${id}.html"${active === id ? ` aria-current="${title === name ? 'page' : 'true'}"` : ''}><span class="nav-number" aria-hidden="true">0${i+1}</span>${name}</a>`).join('');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="${esc(description || 'Geography, peoples, language and cosmology of Erde and Dverghamar.')}"><meta name="color-scheme" content="light dark"><title>${esc(title)} · Erde &amp; Dverghamar</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><script src="assets/theme.js"></script><link rel="stylesheet" href="assets/styles.css"><script src="assets/app.js" defer></script></head><body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="shell"><aside class="sidebar"><a class="brand" href="index.html" aria-label="Erde and Dverghamar, home">${logo}<span>Erde &amp; Dverghamar<small>WORLD GUIDE</small></span></a><nav aria-label="Main navigation"><a href="index.html"${active === 'home' ? ' aria-current="page"' : ''}><span class="nav-number" aria-hidden="true">⌂</span>Overview</a>${nav}</nav><div class="sidebar-note"><span class="small-label">A guide to the setting</span><p>Geography, peoples, language<br>and cosmology.</p><a href="about.html"${active === 'about' ? ' aria-current="page"' : ''}>About this guide</a></div></aside>
  <div class="workspace"><header class="topbar"><span>${active === 'home' ? 'World guide' : esc(pageTitles[active] || title)}</span><div class="header-actions"><button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false" hidden><span aria-hidden="true">◐</span> Dark theme</button><a class="search-link" href="search.html"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="6.5" stroke="currentColor" stroke-width="1.7"/><path d="m15 15 6 6" stroke="currentColor" stroke-width="1.7"/></svg>Search</a></div></header><div class="reading-layout${toc ? ' has-toc' : ''}"><main id="main" tabindex="-1">${body}</main>${toc ? `<aside class="toc"><nav aria-label="On this page"><h2>On this page</h2>${toc}</nav></aside>` : ''}</div><footer><span>Erde &amp; Dverghamar · World guide</span><a href="about.html#sources">Sources &amp; scope</a><a href="https://github.com/Andeleidun/test-fantasy-world${file ? '/blob/main/content/public/'+esc(file) : ''}">${file ? 'View page source' : 'View repository'}</a></footer></div></div></body></html>`;
}
const card = item => `<article class="entry-card"><span class="eyebrow">${esc(item.kind || 'Guide')}</span><h3><a href="${item.id}.html">${esc(item.title)}<span aria-hidden="true"> ↗</span></a></h3><p>${esc(item.description)}</p></article>`;
const intro = (label, title, description) => `<div class="page-intro"><p class="eyebrow">${esc(label)}</p><h1>${esc(title)}</h1><p class="lead">${esc(description)}</p></div>`;
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
await cp('assets', resolve(out, 'assets'), { recursive: true });
await cp('content/public/data', resolve(out, 'data'), { recursive: true });
const columns = ['lemma', 'pos', 'meaning', 'domain', 'parts', 'notes'];
const tsvCell = value => String(value ?? '').replace(/[\t\r\n]+/g, ' ');
await writeFile(resolve(out, 'data/korvar-lexicon.tsv'), [columns.join('\t'), ...lexicon.map(word => columns.map(key => tsvCell(word[key])).join('\t'))].join('\n') + '\n');
await writeFile(resolve(out, '.nojekyll'), '');
async function emit(name, html) { await writeFile(resolve(out, name + '.html'), html); }

const worlds = `<div class="world-cards"><a class="world-card erde" href="erde.html"><div class="world-art" aria-hidden="true"><div class="orb erde-orb"></div><span class="orbit"></span></div><span class="eyebrow">01 / The human world</span><h2>Erde</h2><p>A changed planetary orientation, branching human and hobbit lineages, and regional histories.</p><span class="card-action">Read about Erde <span aria-hidden="true">→</span></span></a><a class="world-card dverghamar" href="dverghamar.html"><div class="world-art" aria-hidden="true"><div class="orb dwarf-orb"></div><span class="orbit"></span></div><span class="eyebrow">02 / The dwarven world</span><h2>Dverghamar</h2><p>A world of permanent day and night, with life gathered across a fragmented twilight region.</p><span class="card-action">Read about Dverghamar <span aria-hidden="true">→</span></span></a></div>`;
await emit('index', layout('World guide', 'home', `${intro('World guide', 'Erde & Dverghamar', 'A guide to the geography, living communities, languages and cosmology of two worlds. Choose a planet for an introduction, or browse a subject below.')}${worlds}<section class="section-block" aria-labelledby="explore-title"><div class="section-heading"><h2 id="explore-title">Browse by subject</h2></div><div class="entry-grid">${['hamarkorar','otherworld','korvar','erde-atlas'].map(id => card(catalog.find(p => p.id === id))).join('')}</div></section><aside class="note"><strong>Reading the maps</strong><p>The atlas shows planetary orientation, habitats and settlement systems. Captions explain where a landscape is illustrative or a climate range remains provisional.</p><a href="about.html">About this guide <span aria-hidden="true">→</span></a></aside>`));

for (const [id, name, title, description] of sections) {
  let body = intro(name, title, description);
  if (id === 'worlds') body += worlds;
  const entries = catalog.filter(p => p.category === id && !(id === 'worlds' && ['erde','dverghamar'].includes(p.id)));
  body += `<div class="entry-grid">${entries.map(card).join('')}</div>`;
  if (id === 'language') body += `<a class="feature-link" href="dictionary.html"><strong>Browse the Korvar dictionary</strong><span>${lexicon.length} lexical records, with meanings and usage notes →</span></a>`;
  if (id === 'maps') body += `<aside class="note"><strong>Read the maps as models.</strong><p>Some maps describe planetary geometry; others illustrate habitats and processes. Their captions explain the scale and scope of each view.</p></aside>`;
  await emit(id, layout(name, id, body, { description }));
}

for (const page of catalog) {
  const source = await readFile(`content/public/${page.file}`, 'utf8');
  const tokens = md.parse(source.replace(/^# [^\n]+\n+/, ''), {});
  const headings = [], used = new Map();
  let current = { title: page.title, href: `${page.id}.html`, text: page.description, category: page.category };
  const chunks = [current];
  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];
    if (token.type === 'heading_open') {
      const title = tokens[i+1].content;
      const base = slug(title); const n = (used.get(base) || 0) + 1; used.set(base, n);
      const anchor = base + (n > 1 ? `-${n}` : '');
      token.attrSet('id', anchor);
      // The page template owns h1; source headings begin at h2.
      if (token.tag === 'h1') { token.tag = 'h2'; tokens[i+2].tag = 'h2'; }
      if (token.tag === 'h2') {
        headings.push({ title, anchor });
        current = { title: `${page.title}: ${title}`, href: `${page.id}.html#${anchor}`, text: '', category: page.category };
        chunks.push(current);
      }
    }
    if (token.type === 'inline') current.text += ' ' + (token.children || []).map(child => ['text', 'code_inline', 'image'].includes(child.type) ? child.content : ['softbreak', 'hardbreak'].includes(child.type) ? ' ' : '').join('');
  }
  searchIndex.push(...chunks.filter(c => c.text.trim()));
  let html = md.renderer.render(tokens, md.options, {});
  // A labeled, keyboard-focusable scroll region keeps wide reference tables usable.
  html = html.replace(/<table>/g, '<div class="table-scroll" role="region" aria-label="Reference table" tabindex="0"><table>').replace(/<\/table>/g, '</table></div>');
  if (page.id === 'language-writing') html += '<figure><a href="assets/Stavmark.svg"><img src="assets/Stavmark.svg" alt="Stavmark alphabet reference: 24 basic signs, two regional extensions, decimal figures and a sample phrase" width="960" height="920" loading="lazy"></a><figcaption>The current Stavmark sign chart. <a href="assets/Stavmark.svg">Open the full-size writing reference</a>.</figcaption></figure>';
  const mapRows = maps.filter(m => m.world === (page.id === 'erde-atlas' ? 'Erde' : page.id === 'dverghamar-atlas' ? 'Dverghamar' : ''));
  if (mapRows.length) html += mapRows.map(m => `<figure id="${m.code.toLowerCase()}"><a href="assets/maps/${m.stem}.svg" aria-label="Open full-size map: ${esc(m.title)}"><img src="assets/maps/${m.stem}.svg" alt="${esc(m.description)}" loading="lazy" width="${m.width}" height="${m.height}"></a><figcaption><strong>${esc(m.code)} · ${esc(m.title)}</strong><p>${esc(m.description)}</p><p class="map-reading">${esc(m.reading)}</p><a href="assets/maps/${m.stem}.svg">Open full-size map</a></figcaption></figure>`).join('');
  searchIndex.push(...mapRows.map(m => ({ title: m.title, category: 'maps', href: `${page.id}.html#${m.code.toLowerCase()}`, text: `${m.description} ${m.reading}` })));
  const toc = headings.map(h => `<a href="#${h.anchor}">${esc(h.title)}</a>`).join('') + mapRows.map(m => `<a href="#${m.code.toLowerCase()}">${esc(m.code)} · ${esc(m.title)}</a>`).join('');
  await emit(page.id, layout(page.title, page.category, `${intro(page.kind, page.title, page.description)}${toc ? `<details class="mobile-toc"><summary>On this page</summary><nav aria-label="Article sections">${toc}</nav></details>` : ""}<article class="prose">${html}</article><div class="article-end"><a href="${page.category}.html">← Back to ${esc(pageTitles[page.category])}</a><a href="#main">Back to top ↑</a></div>`, { toc, description: page.description, file: page.file }));
}

const rows = lexicon.map((word, i) => {
  searchIndex.push({ title: word.lemma, href: `dictionary.html#word-${i}`, category: 'language', text: `${word.meaning} ${word.parts} ${word.notes}` });
  return `<tr id="word-${i}"><th scope="row">${esc(word.lemma)}<small>${esc(word.pos)}</small></th><td>${esc(word.meaning)}<small>${esc(word.domain)}</small></td><td><code>${esc(word.parts || '—')}</code><p>${esc(word.notes)}</p></td></tr>`;
}).join('');
await emit('dictionary', layout('Korvar dictionary', 'language', `${intro('Language / Dictionary', 'The Korvar dictionary', `${lexicon.length} lexical records with definitions and usage notes. People and language names appear in lowercase lookup form.`)}<div class="prose"><p>N = noun; V = infinitive; ADJ = adjective; ADV = adverb; PREP = preposition; PRON = pronoun; DET = determiner; CONJ = conjunction; PART = particle; Q = question word; REL = relative; RESP = response; NUM = number; BOUND = bound form.</p></div><div class="dictionary-tools" hidden><label for="dictionary-query">Find a word or meaning</label><input id="dictionary-query" type="search" placeholder="Try stone, hamarkor, or water"><p id="dictionary-status" role="status"></p></div><div class="table-scroll" role="region" aria-label="Korvar dictionary" tabindex="0"><table id="dictionary"><caption>Common forms, meanings and usage</caption><thead><tr><th scope="col">Word</th><th scope="col">Meaning</th><th scope="col">Formation &amp; usage</th></tr></thead><tbody>${rows}</tbody></table></div>`));

await emit('search', layout('Search the lore', 'search', `${intro('World guide', 'Search the guide', 'Find topics in the public articles, map captions and Korvar dictionary.')}<form class="search-form" role="search" action="search.html" method="get"><div><label for="query">Search the lore</label><input type="search" name="q" id="query" placeholder="Try Thals, planetary spirits, or Hamarkor" maxlength="200"></div><div><label for="category">Within</label><select name="category" id="category"><option value="">Everything</option>${sections.map(([id,name])=>`<option value="${id}">${name}</option>`).join('')}</select></div><button type="submit">Search</button></form><noscript><p>Search needs JavaScript. All lore remains available through the navigation and topic indexes.</p></noscript><p id="search-status" role="status" aria-live="polite">Enter a word or phrase to explore the lore.</p><ol id="results" class="search-results"></ol><button id="more-results" class="secondary-button" hidden>Show more results</button>`));
await writeFile(resolve(out, 'search-index.json'), JSON.stringify(searchIndex));
await emit('about', layout('About this guide', 'about', `${intro('World guide', 'About this guide', 'A public reference to the setting of Erde and Dverghamar.')}<article class="prose"><h2 id="scope">What you’ll find here</h2><p>The guide brings together geography, ecology, peoples, languages and cosmology. Start with a planet overview, then follow links to more detailed subjects. The atlas and dictionary can also be read independently.</p><p>Some parts of the setting are still taking shape. Articles identify provisional physical models, unassigned names and other open details where they affect the description. A proposed climate range is not a completed planetary simulation.</p><h2 id="sources">Sources and the public edition</h2><p>These articles form a separately edited public edition of the project’s worldbuilding documents. The longer working sources retain their development history in the repository. <a href="https://github.com/Andeleidun/test-fantasy-world/tree/main/content/public">Read the public documents</a> or consult the <a href="https://github.com/Andeleidun/test-fantasy-world/blob/main/content/SOURCES.md">source notes</a>.</p><p>The atlas retains its original diagrams with explanatory captions. Korvar’s dictionary, regional forms and translated examples accompany the language guide.</p><h2 id="accessibility">Reading preferences</h2><p>The guide follows your device’s light or dark appearance until you choose a theme with the header toggle. That choice is remembered in this browser when browser storage is available. Maps retain their original light artwork; printed pages use a light background.</p><p>Articles, maps and the complete dictionary remain available without JavaScript. Search and dictionary filtering use JavaScript. Keyboard navigation includes a skip link, visible focus and scrollable reference tables. Every map has a text explanation and a full-size link.</p></article>`));
await emit('404', layout('Page not found', '', `${intro('404', 'Page not found', 'The page may have moved, or the address may be incomplete.')}<p><a href="/test-fantasy-world/">Return to the world guide</a></p>`).replace("<head>", '<head><base href="/test-fantasy-world/">'));
console.log(`Built ${catalog.length} articles, ${maps.length} maps and ${lexicon.length} dictionary records.`);
