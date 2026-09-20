import { readFile, writeFile, mkdir, rm, cp } from 'node:fs/promises';
import { resolve } from 'node:path';
import MarkdownIt from 'markdown-it';
import { catalog, articleSources, publicLink, readerAssets, wordAnchor, legacyWordAnchor, related } from './public-edition.mjs';

const out = resolve('dist');
const maps = JSON.parse(await readFile('content/public/maps.json', 'utf8'));
const lexicon = JSON.parse(await readFile('content/public/lexicon.json', 'utf8'));
const esc = value => String(value).replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[c]);
const md = new MarkdownIt({ html: false, linkify: false, typographer: false });
const renderLink = md.renderer.rules.link_open || ((tokens, i, options, env, self) => self.renderToken(tokens, i, options));
md.renderer.rules.link_open = (tokens, i, options, env, self) => {
  const href = tokens[i].attrGet('href');
  if (href) tokens[i].attrSet('href', publicLink(href));
  return renderLink(tokens, i, options, env, self);
};
const slug = value => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section';
const sections = [
  ['worlds', 'Worlds', 'The inhabited worlds', 'The landscapes, climates and deep histories of Erde, Dverghamar, Merenval and Merenval’s companion.'],
  ['peoples', 'Peoples', 'Peoples and natural history', 'The peoples of the inhabited worlds, their ancestry and ways of life.'],
  ['cosmology', 'Magic & belief', 'The Otherworld, magic and belief', 'How people learn and use magic, seek spiritual contact and tell stories about the Otherworld.'],
  ['language', 'Language', 'The speech of the Hamarkorar', 'Learn Korvar pronunciation and grammar, compare five regional languages, or look up a word.'],
  ['maps', 'Atlas', 'The public atlas guides', 'Thirteen text entries cover the geography of Erde and Dverghamar. Map illustrations are awaiting revision.'],
  ['reference', 'References', 'Cultural histories and references', 'Longer histories and naturalist accounts, with an index of the collection.']
];
const pageTitles = Object.fromEntries(sections.map(([id, name]) => [id, name]));
const searchIndex = [];
const sectionAnchors = JSON.parse(await readFile('content/section-anchors.json', 'utf8'));
const renderHeading = md.renderer.rules.heading_open || ((tokens, i, options, env, self) => self.renderToken(tokens, i, options));
md.renderer.rules.heading_open = (tokens, i, options, env, self) =>
  (tokens[i].meta?.aliases || []).map(id => `<span id="${esc(id)}" aria-hidden="true"></span>`).join('') + renderHeading(tokens, i, options, env, self);
const logo = '<svg viewBox="0 0 32 36" width="28" height="32" fill="none" aria-hidden="true"><path d="M16 2 30 10v16L16 34 2 26V10Z" stroke="currentColor" stroke-width="1.5"/><path d="m7 24 9-15 9 15M11 18h10M16 9v22" stroke="currentColor" stroke-width="1.5"/></svg>';
function layout(title, active, body, { toc = '', description = '', file = '' } = {}) {
  const nav = sections.map(([id, name], i) => `<a href="${id}.html"${active === id ? ` aria-current="${title === name ? 'page' : 'true'}"` : ''}><span class="nav-number" aria-hidden="true">0${i+1}</span>${name}</a>`).join('');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="${esc(description || 'Landscapes, peoples, language, magic and belief across Erde, Dverghamar and Merenval.')}"><meta name="color-scheme" content="light dark"><title>${esc(title)} · Erde, Dverghamar &amp; Merenval</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><script src="assets/theme.js"></script><link rel="stylesheet" href="assets/styles.css"><script src="assets/app.js" defer></script></head><body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="shell"><aside class="sidebar"><a class="brand" href="index.html" aria-label="Erde, Dverghamar and Merenval, home">${logo}<span>Erde · Dverghamar · Merenval<small>WORLD GUIDE</small></span></a><nav aria-label="Main navigation"><a href="index.html"${active === 'home' ? ' aria-current="page"' : ''}><span class="nav-number" aria-hidden="true">⌂</span>Overview</a>${nav}</nav><div class="sidebar-note"><span class="small-label">A guide to the setting</span><p>Geography, peoples, language,<br>magic and belief.</p><a href="about.html"${active === 'about' ? ' aria-current="page"' : ''}>About this guide</a></div></aside>
  <div class="workspace"><header class="topbar"><span>${active === 'home' ? 'World guide' : esc(pageTitles[active] || title)}</span><div class="header-actions"><button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false" hidden><span aria-hidden="true">◐</span> Dark theme</button><a class="search-link" href="search.html"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="6.5" stroke="currentColor" stroke-width="1.7"/><path d="m15 15 6 6" stroke="currentColor" stroke-width="1.7"/></svg>Search</a></div></header><div class="reading-layout${toc ? ' has-toc' : ''}"><main id="main" tabindex="-1">${body}</main>${toc ? `<aside class="toc"><nav aria-label="On this page"><h2>On this page</h2>${toc}</nav></aside>` : ''}</div><footer><span>Erde · Dverghamar · Merenval · World guide</span><a href="about.html#sources">Sources &amp; scope</a><a href="https://github.com/Andeleidun/test-fantasy-world${file ? '/blob/main/content/public/'+esc(file) : ''}">${file ? 'View page source' : 'View repository'}</a></footer></div></div></body></html>`;
}
const card = item => `<article class="entry-card"><span class="eyebrow">${esc(item.kind || 'Guide')}</span><h3><a href="${item.id}.html">${esc(item.title)}</a></h3><p>${esc(item.description)}</p></article>`;
const intro = (label, title, description) => `<div class="page-intro"><p class="eyebrow">${esc(label)}</p><h1>${esc(title)}</h1><p class="lead">${esc(description)}</p></div>`;
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
await mkdir(resolve(out, 'assets'));
for (const file of readerAssets) await cp(`assets/${file}`, resolve(out, 'assets', file));
for (const file of ['catalog.json', 'maps.json', 'lexicon.json', 'PUBLIC-INDEX.txt']) await cp(`content/public/${file}`, resolve(out, file));
await cp('content/public/data', resolve(out, 'data'), { recursive: true });
await writeFile(resolve(out, '.nojekyll'), '');
async function emit(name, html) { await writeFile(resolve(out, name + '.html'), html); }

const worlds = `<div class="world-cards"><a class="world-card erde" href="erde.html"><div class="world-art" aria-hidden="true"><div class="orb erde-orb"></div><span class="orbit"></span></div><span class="eyebrow">01 / The human world</span><h2>Erde</h2><p>Continental landscapes and the histories of Humans, hobbit lineages and diverse Goblin peoples.</p><span class="card-action">Read about Erde <span aria-hidden="true">→</span></span></a><a class="world-card dverghamar" href="dverghamar.html"><div class="world-art" aria-hidden="true"><div class="orb dwarf-orb"></div><span class="orbit"></span></div><span class="eyebrow">02 / The twilight world</span><h2>Dverghamar</h2><p>Permanent day and night, with Hamarkorar, Thals and Jotun in twilight and mountain settlements.</p><span class="card-action">Read about Dverghamar <span aria-hidden="true">→</span></span></a><a class="world-card merenval" href="merenval.html"><div class="world-art" aria-hidden="true"><div class="orb merenval-orb"></div><span class="companion-orb"></span><span class="orbit"></span></div><span class="eyebrow">03 / The paired worlds</span><h2>Merenval</h2><p>A water-rich Elven world and its inhabited companion, home also to Gnomes and Orcs.</p><span class="card-action">Read about Merenval <span aria-hidden="true">→</span></span></a></div>`;
await emit('index', layout('World guide', 'home', `${intro('World guide', 'Erde, Dverghamar & Merenval', 'Three worlds and an inhabited companion, with their own peoples, languages and histories. Choose a world or a subject to begin.')}${worlds}<section class="section-block" aria-labelledby="explore-title"><div class="section-heading"><h2 id="explore-title">Browse by subject</h2></div><div class="entry-grid">${['elves','stellar-system-reference','magic','otherworld','korvar'].map(id => card(catalog.find(p => p.id === id))).join('')}</div></section>`));

for (const [id, name, title, description] of sections) {
  let body = intro(name, title, description);
  if (id === 'worlds') body += worlds;
  const entries = catalog.filter(p => p.category === id && !(id === 'worlds' && ['erde','dverghamar','merenval'].includes(p.id)));
  body += `<div class="entry-grid">${entries.map(card).join('')}</div>`;
  if (id === 'language') body += `<a class="feature-link" href="dictionary.html"><strong>Browse the Korvar dictionary</strong><span>${lexicon.length} lexical records, with meanings and usage notes →</span></a>`;
  if (id === 'maps') body += `<aside class="note"><strong>Atlas illustrations</strong><p>The atlas currently has text entries. Its illustrations are awaiting revision.</p></aside>`;
  await emit(id, layout(name, id, body, { description }));
}

for (const page of catalog) {
  const source = articleSources.get(page.file);
  const tokens = md.parse(source.replace(/^# [^\n]+\n+/, ''), {});
  const headings = [], used = new Map();
  let current = { title: page.title, href: `${page.id}.html`, text: page.description, category: page.category };
  const chunks = [current];
  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];
    if (token.type === 'heading_open') {
      const title = tokens[i+1].content;
      const base = slug(title); const n = (used.get(base) || 0) + 1; used.set(base, n);
      const mapSubject = maps.find(map => map.guide === page.file && title.startsWith(map.code + ' ·'));
      const anchor = mapSubject ? mapSubject.code.toLowerCase() : base + (n > 1 ? `-${n}` : '');
      token.attrSet('id', anchor);
      token.meta = { aliases: Object.entries(sectionAnchors[page.id] || {}).filter(([, target]) => target === anchor).map(([old]) => old) };
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
  if (page.id === 'language-writing') html += '<figure><a href="assets/Stavmark.svg"><img src="assets/Stavmark.svg" alt="Stavmark alphabet reference: 24 basic signs, two regional extensions, decimal figures and a sample phrase" width="960" height="920" loading="lazy"></a><figcaption>The Stavmark alphabet. <a href="assets/Stavmark.svg">Open the full-size writing reference</a>.</figcaption></figure>';
  const toc = headings.map(h => `<a href="#${h.anchor}">${esc(h.title)}</a>`).join('');
  const reading = (related[page.id] || []).map(id => catalog.find(item => item.id === id));
  if (reading.length) html += `<nav aria-label="Related reading"><h2>Related reading</h2><ul>${reading.map(item => `<li><a href="${item.id}.html">${esc(item.title)}</a></li>`).join('')}</ul></nav>`;
  await emit(page.id, layout(page.title, page.category, `${intro(page.kind, page.title, page.description)}${toc ? `<details class="mobile-toc"><summary>On this page</summary><nav aria-label="Article sections">${toc}</nav></details>` : ""}<article class="prose">${html}</article><div class="article-end"><a href="${page.category}.html">← Back to ${esc(pageTitles[page.category])}</a><a href="#main">Back to top ↑</a></div>`, { toc, description: page.description, file: page.file }));
}

const rows = lexicon.map(word => {
  searchIndex.push({ title: word.lemma, href: `dictionary.html#${wordAnchor(word)}`, category: 'language', text: `${word.meaning} ${word.parts} ${word.notes}` });
  return `<tr id="${wordAnchor(word)}"><th scope="row">${legacyWordAnchor(word) ? `<span id="${legacyWordAnchor(word)}"></span>` : ''}${esc(word.lemma)}<small>${esc(word.pos)}</small></th><td>${esc(word.meaning)}<small>${esc(word.domain)}</small></td><td><code>${esc(word.parts || '—')}</code><p>${esc(word.notes)}</p></td></tr>`;
}).join('');
await emit('dictionary', layout('Korvar dictionary', 'language', `${intro('Language / Dictionary', 'The Korvar dictionary', `${lexicon.length} lexical records with definitions and usage notes. People and language names appear in lowercase lookup form.`)}<div class="prose"><p>N = noun; V = infinitive; ADJ = adjective; ADV = adverb; PREP = preposition; PRON = pronoun; DET = determiner; CONJ = conjunction; PART = particle; Q = question word; REL = relative; RESP = response; NUM = number; BOUND = bound form.</p></div><div class="dictionary-tools" hidden><label for="dictionary-query">Find a word or meaning</label><input id="dictionary-query" type="search" placeholder="Try stone, hamarkor, or water"><p id="dictionary-status" role="status"></p></div><div class="table-scroll" role="region" aria-label="Korvar dictionary" tabindex="0"><table id="dictionary"><caption>Common forms, meanings and usage</caption><thead><tr><th scope="col">Word</th><th scope="col">Meaning</th><th scope="col">Formation &amp; usage</th></tr></thead><tbody>${rows}</tbody></table></div>`));

await emit('search', layout('Search the lore', 'search', `${intro('World guide', 'Search the guide', 'Find topics in the public articles, atlas reading notes and Korvar dictionary.')}<form class="search-form" role="search" action="search.html" method="get"><div><label for="query">Search the lore</label><input type="search" name="q" id="query" placeholder="Try Thals, household, or Hamarkor" maxlength="200"></div><div><label for="category">Within</label><select name="category" id="category"><option value="">Everything</option>${sections.map(([id,name])=>`<option value="${id}">${name}</option>`).join('')}</select></div><button type="submit">Search</button></form><noscript><p>Search needs JavaScript. All lore remains available through the navigation and topic indexes.</p></noscript><p id="search-status" role="status" aria-live="polite">Enter a word or phrase to search.</p><ol id="results" class="search-results"></ol><button id="more-results" class="secondary-button" hidden>Show more results</button>`));
await writeFile(resolve(out, 'search-index.json'), JSON.stringify(searchIndex));
await emit('about', layout('About this guide', 'about', `${intro('World guide', 'About this guide', 'A guide to the worlds, peoples and languages of the setting.')}<article class="prose"><h2 id="scope">What you’ll find here</h2><p>The articles describe landscapes, peoples, histories, languages and everyday magic. Naturalists compare bodies and habitats using methods within the reach of nineteenth-century scholarship. Spiritual accounts follow ordinary trained practitioners; Otherworld stories record what human travelers report.</p><p>The accounts distinguish observations from theories and religious beliefs. Origins, spiritual encounters and many local histories remain uncertain or undescribed.</p><h2 id="sources">Sources and the public edition</h2><p>This edition follows the current <a href="https://drive.google.com/drive/folders/126BrWsD3GZ-Qg2oGTjxX3lN_Tp642AXt">public source collection</a>, edited and synchronized on 20 September 2026. Browse the <a href="README.html">complete collection index</a> or the <a href="reference.html">cultural references</a>. Earlier technical drafts and maps remain in the repository’s research archive.</p><p>All original project IP remains the author’s. Public documentation grants no license or right to reuse the work.</p><h2 id="downloads">Language data and indexes</h2><ul><li><a href="data/korvar-lexicon.tsv">Korvar dictionary (TSV)</a></li><li><a href="data/regional-dictionary.tsv">Regional dictionary (TSV)</a></li><li><a href="data/korvar-examples.tsv">Translated examples (TSV)</a></li><li><a href="lexicon.json">Lexicon (JSON)</a></li><li><a href="maps.json">Atlas subjects (JSON)</a></li><li><a href="catalog.json">Document catalog (JSON)</a></li><li><a href="PUBLIC-INDEX.txt">Source collection index (text)</a></li></ul><p>The collection contains ${catalog.length - 1} subject articles, an index, ${lexicon.length} dictionary records and thirteen atlas entries. The atlas is currently text only.</p><h2 id="accessibility">Reading preferences</h2><p>The guide follows your device’s light or dark appearance until you choose a theme. That choice is remembered when browser storage is available. Printed pages use a light background.</p><p>Articles, atlas notes, downloads and the complete dictionary remain available without JavaScript. Search and dictionary filtering use JavaScript. Keyboard navigation includes a skip link, visible focus and scrollable reference tables. The Stavmark writing chart has an accompanying text explanation and full-size link.</p></article>`));
await emit('404', layout('Page not found', '', `${intro('404', 'Page not found', 'The page may have moved, or the address may be incomplete.')}<p><a href="/test-fantasy-world/">Return to the world guide</a></p>`).replace("<head>", '<head><base href="/test-fantasy-world/">'));
console.log(`Built ${catalog.length} articles, ${maps.length} atlas subjects and ${lexicon.length} dictionary records.`);
