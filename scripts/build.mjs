import { readFile, writeFile, mkdir, rm, cp } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import MarkdownIt from 'markdown-it';
import { catalog, wordAnchor, legacyWordAnchor } from './public-edition.mjs';
import { guides, figures, readerFiles, routes, coverage, sourceSections, readerLink, extraChapters } from './reader-edition.mjs';

const out=resolve('dist');
const lexicon=JSON.parse(await readFile('content/public/lexicon.json','utf8'));
const atlas=JSON.parse(await readFile('content/public/maps.json','utf8'));
const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const md=new MarkdownIt({html:false,linkify:false,typographer:false});
const renderLink=md.renderer.rules.link_open||((tokens,i,options,env,self)=>self.renderToken(tokens,i,options));
md.renderer.rules.link_open=(tokens,i,options,env,self)=>{
  const href=tokens[i].attrGet('href');
  if(href) tokens[i].attrSet('href',readerLink(href));
  return renderLink(tokens,i,options,env,self);
};
const searchIndex=[];
const rights='All original project IP remains the author’s. Public documentation grants no license or right to reuse this work.';
const intro=(label,title,description)=>`<div class="page-intro"><p class="eyebrow">${esc(label)}</p><h1>${esc(title)}</h1><p class="lead">${esc(description)}</p></div>`;
const figure=id=>{
  const item=figures.find(f=>f.id===id);
  if(!item) throw new Error(`Missing figure ${id}`);
  return `<figure id="figure-${item.id}" class="${item.kind}"><a href="assets/${item.file}" aria-label="Open full-size image: ${esc(item.id.replaceAll('-',' '))}"><img src="assets/${item.file}" alt="${esc(item.alt)}" width="${item.width}" height="${item.height}" loading="lazy" decoding="async"></a><figcaption>${esc(item.caption)} <a href="assets/${item.file}">View full size</a>.</figcaption></figure>`;
};
function layout(title,active,body,{toc='',description='',canonical='',compatibility=false}={}) {
  const nav=guides.map(guide=>`<a href="${guide.id}.html"${active===guide.id?' aria-current="page"':''}>${esc(guide.label)}</a>`).join('');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="${esc(description||'The worlds, peoples and languages of Erde, Dverghamar and Merenval.')}"><meta name="color-scheme" content="light dark"><title>${esc(title)} · World guide</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml">${canonical?`<link rel="canonical" href="https://andeleidun.github.io/test-fantasy-world/${esc(canonical)}">`:''}${compatibility?'<meta name="robots" content="noindex">':''}<script src="assets/theme.js"></script><link rel="stylesheet" href="assets/styles.css"><script src="assets/app.js" defer></script></head><body>
<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-row"><a class="site-brand" href="index.html">Erde · Dverghamar · Merenval<small>World guide</small></a><div class="header-actions"><button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false" hidden><span aria-hidden="true">◐</span> Dark theme</button><a class="search-link" href="search.html">Search</a></div></div><nav class="guide-nav" aria-label="Main navigation">${nav}</nav></header>
<div class="reading-layout${toc?' has-toc':''}"><main id="main" tabindex="-1">${body}</main>${toc?`<aside class="toc"><nav aria-label="On this page"><h2>Contents</h2>${toc}</nav><a class="toc-top" href="#main">Back to top</a></aside>`:''}</div><footer><p>${rights}</p><a href="about.html">About and sources</a><a href="about.html#downloads">Downloads</a><a href="https://github.com/Andeleidun/test-fantasy-world">Repository</a></footer></body></html>`;
}
const prose=value=>md.render(value).replace(/<table>/g,'<div class="table-scroll" role="region" aria-label="Reference table" tabindex="0"><table>').replace(/<\/table>/g,'</table></div>');
const plain=value=>md.parse(value,{}).filter(t=>t.type==='inline').map(t=>(t.children||[]).map(c=>['text','code_inline','image'].includes(c.type)?c.content:['softbreak','hardbreak'].includes(c.type)?' ':'').join('')).join(' ');
await rm(out,{recursive:true,force:true});
await mkdir(out,{recursive:true});
for(const file of readerFiles){ await mkdir(dirname(resolve(out,'assets',file)),{recursive:true}); await cp(`assets/${file}`,resolve(out,'assets',file)); }
for(const file of ['catalog.json','maps.json','lexicon.json','PUBLIC-INDEX.txt']) await cp(`content/public/${file}`,resolve(out,file));
await cp('content/public/data',resolve(out,'data'),{recursive:true});
await mkdir(resolve(out,'guides'),{recursive:true});
await mkdir('guides',{recursive:true});
await writeFile(resolve(out,'.nojekyll'),'');
const emit=(name,html)=>writeFile(resolve(out,name+'.html'),html);

function chapterContent(chapter,guideId) {
  let html='',markdown='',detailLinks='';
  for(const sourceId of chapter.sources) {
    const page=catalog.find(p=>p.id===sourceId);
    for(const section of sourceSections.get(sourceId)) {
      if(section.omitted) continue;
      const level=Math.min(section.level,6);
      if(section.oldAnchor) {
        html+=`<h${level} id="${section.anchor}">${esc(section.title)}</h${level}>`;
        markdown+=`\n<a id="${section.anchor}"></a>\n${'#'.repeat(level)} ${section.title}\n\n`;
        if(level===3 && section.text) detailLinks+=`<a href="#${section.anchor}">${esc(section.title)}</a>`;
      }
      html+=prose(section.text);
      markdown+=section.text+'\n\n';
      if(section.text) searchIndex.push({title:`${page.title}${section.oldAnchor?': '+section.title:''}`,href:`${guideId}.html#${section.anchor}`,category:page.category,guide:guideId,text:plain(section.text)});
      const added=figures.filter(f=>f.after===`${sourceId}#${section.oldAnchor}`);
      for(const item of added) {
        html+=figure(item.id);
        markdown+=`<a id="figure-${item.id}"></a>\n![${item.alt}](../assets/${item.file})\n\n${item.caption}\n\n`;
      }
      const map=atlas.find(m=>m.guide===page.file && m.code.toLowerCase()===section.oldAnchor);
      const shared=map && figures.find(f=>f.codes?.includes(map.code));
      if(shared && !added.includes(shared)) {
        html+=`<p class="figure-reference"><a href="#figure-${shared.id}">See the ${esc(shared.id.replace(guideId+'-','').replaceAll('-',' '))} diagram</a>.</p>`;
        markdown+=`[See the diagram](#figure-${shared.id}).\n\n`;
      }
    }
  }
  return {html,markdown,detailLinks};
}
const dictionaryRows=lexicon.map(word=>{
  const anchor=wordAnchor(word);
  routes['dictionary.html'][anchor]=`korvar.html#${anchor}`;
  if(legacyWordAnchor(word)) routes['dictionary.html'][legacyWordAnchor(word)]=`korvar.html#${legacyWordAnchor(word)}`;
  searchIndex.push({title:word.lemma,href:`korvar.html#${anchor}`,category:'language',guide:'korvar',text:`${word.meaning} ${word.parts} ${word.notes}`});
  return `<tr id="${anchor}"><th scope="row">${legacyWordAnchor(word)?`<span id="${legacyWordAnchor(word)}"></span>`:''}${esc(word.lemma)}<small>${esc(word.pos)}</small></th><td>${esc(word.meaning)}<small>${esc(word.domain)}</small></td><td><code>${esc(word.parts||'—')}</code><p>${esc(word.notes)}</p></td></tr>`;
}).join('');
const dictionaryHTML=`<p>N = noun; V = infinitive; ADJ = adjective; ADV = adverb; PREP = preposition; PRON = pronoun; DET = determiner; CONJ = conjunction; PART = particle; Q = question word; REL = relative; RESP = response; NUM = number; BOUND = bound form.</p><div class="dictionary-tools" hidden><label for="dictionary-query">Find a word or meaning</label><input id="dictionary-query" type="search" placeholder="Try stone, hamarkor, or water"><p id="dictionary-status" role="status"></p></div><div class="table-scroll" role="region" aria-label="Korvar dictionary" tabindex="0"><table id="dictionary"><caption>562 records: common forms, meanings and usage</caption><thead><tr><th scope="col">Word</th><th scope="col">Meaning</th><th scope="col">Formation and usage</th></tr></thead><tbody>${dictionaryRows}</tbody></table></div>`;
for(const guide of guides) {
  let chapters='',toc='',markdown=`# ${guide.title}\n\n${guide.description}\n\n`;
  if(guide.hero) { const item=figures.find(f=>f.id===guide.hero); markdown+=`![${item.alt}](../assets/${item.file})\n\n${item.caption}\n\n`; }
  for(const [i,chapter] of guide.chapters.entries()) {
    const content=chapterContent(chapter,guide.id);
    const isDictionary=chapter.id==='dictionary-section';
    const jump=`<a href="#${chapter.id}">${esc(chapter.title)}</a>`;
    toc+=`<div class="toc-chapter">${jump}${content.detailLinks?`<details><summary>Sections</summary>${content.detailLinks}</details>`:''}</div>`;
    chapters+=`<section class="guide-chapter" aria-labelledby="${chapter.id}"><p class="chapter-number" aria-hidden="true">${String(i+1).padStart(2,'0')}</p><h2 id="${chapter.id}">${esc(chapter.title)}</h2>${content.html}${isDictionary?dictionaryHTML:''}</section>`;
    markdown+=`<a id="${chapter.id}"></a>\n## ${chapter.title}\n\n${content.markdown}`;
    if(isDictionary) markdown+='| Word | Part of speech | Meaning | Formation | Notes |\n| --- | --- | --- | --- | --- |\n'+lexicon.map(w=>`| ${[w.lemma,w.pos,w.meaning,w.parts,w.notes].map(v=>String(v||'').replaceAll('|','\\|').replaceAll('\n',' ')).join(' | ')} |`).join('\n')+'\n\n';
  }
  // Existing fragments on a guide's original URL remain valid in the consolidated page.
  const own=routes[guide.id+'.html']||{};
  const renderedIds=new Set([...chapters.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
  for(const [old,destination] of Object.entries(own)) {
    if(!old||renderedIds.has(old)) continue;
    const target=destination.split('#')[1];
    if(!target || !renderedIds.has(target)) throw new Error(`Missing in-page alias ${guide.id}#${old}`);
    chapters=chapters.replace(new RegExp(`(<h[2-6] id="${target}"[^>]*>)`),`<span id="${old}" aria-hidden="true"></span>$1`);
  }
  markdown+='\n'+rights+'\n';
  // Resolve source links into the same five-document edition, including local fragments.
  markdown=markdown.replace(/\]\(([^)]+)\)/g,(whole,href)=>{
    const local=readerLink(href);
    if (/^(https?:|#|\.\.\/assets\/)/.test(local)) return `](${local})`;
    const guideLink=guides.some(guide=>local.split('#')[0]===guide.id+'.html');
    return `](${guideLink?local.replace('.html','.md'):'https://andeleidun.github.io/test-fantasy-world/'+local})`;
  });
  await writeFile(`guides/${guide.id}.md`,markdown);
  await writeFile(resolve(out,'guides',guide.id+'.md'),markdown);
  const contents=`<details class="mobile-toc"><summary>Contents: ${guide.chapters.length} chapters</summary><nav aria-label="Guide chapters">${toc}</nav></details>`;
  await emit(guide.id,layout(guide.title,guide.id,`${intro('World guide',guide.title,guide.description)}${contents}<p class="guide-download"><a href="guides/${guide.id}.md" download>Download this guide</a></p>${guide.hero?figure(guide.hero):''}<article class="prose">${chapters}</article><div class="article-end"><a href="index.html#guides">All five guides</a><a href="#main">Back to top</a></div>`,{toc,description:guide.description,canonical:guide.id+'.html'}));
}

const cards=guides.map((guide,i)=>`<article class="guide-card">${guide.hero?`<a href="${guide.id}.html" tabindex="-1" aria-hidden="true"><img src="assets/${figures.find(f=>f.id===guide.hero).file}" alt="" width="1536" height="1024" loading="lazy"></a>`:''}<div><p class="eyebrow">Guide ${i+1}</p><h2><a href="${guide.id}.html">${esc(guide.label)}</a></h2><p>${esc(guide.description)}</p><ul>${guide.chapters.slice(0,6).map(c=>`<li><a href="${guide.id}.html#${c.id}">${esc(c.title)}</a></li>`).join('')}${guide.id==='korvar'?'<li><a href="korvar.html#dictionary-section">Dictionary and word search</a></li>':''}</ul></div></article>`).join('');
const skies=chapterContent(extraChapters[0],'index');
await emit('index',layout('World guide','home',`${intro('World guide','Erde, Dverghamar & Merenval','Five guides bring the worlds, their peoples and the workings of magic together. Read a complete account or jump to a chapter below.')}<section id="guides" class="guide-grid" aria-label="The five guides">${cards}</section><section class="prose guide-chapter" aria-labelledby="skies"><h2 id="skies">The worlds and their skies</h2>${skies.html}</section><section class="quick-index" id="peoples"><h2>Find a people</h2><p><a href="erde.html#ancestry">Humans and hobbit lineages</a> · <a href="erde.html#goblins">Goblins</a> · <a href="dverghamar.html#hamarkorar">Hamarkorar</a> · <a href="dverghamar.html#thals">Thals</a> · <a href="dverghamar.html#jotuns">Jotun</a> · <a href="merenval.html#elves">Elves</a> · <a href="merenval.html#gnomes">Gnomes</a> · <a href="merenval.html#orcs">Orcs</a></p><h2 id="maps">Maps in the guides</h2><p><a href="erde.html#atlas">Erde: regions, landscape and ancestry</a><br><a href="dverghamar.html#atlas">Dverghamar: light, habitats and mountain homes</a><br><a href="merenval.html#figure-merenval-pair">Merenval and its companion</a></p></section>`,{canonical:'index.html'}));
const categories=[['worlds','Worlds'],['peoples','Peoples'],['cosmology','Magic and belief'],['language','Language'],['maps','Maps'],['reference','Histories and references']];
await emit('search',layout('Search the guide','search',`${intro('World guide','Search the guide','Search the complete text and dictionary. Each result opens the relevant section in its guide.')}<form class="search-form" role="search" action="search.html" method="get"><div><label for="query">Search the lore</label><input type="search" name="q" id="query" placeholder="Try Thals, living houses, or Hamarkor" maxlength="200"></div><div><label for="category">Within</label><select name="category" id="category"><option value="">Everything</option>${categories.map(([id,title])=>`<option value="${id}">${title}</option>`).join('')}</select></div><button type="submit">Search</button></form><noscript><p>Search needs JavaScript. The five guides and their contents lists remain available without it.</p></noscript><p id="search-status" role="status" aria-live="polite">Enter a word or phrase to search.</p><ol id="results" class="search-results"></ol><button id="more-results" class="secondary-button" hidden>Show more results</button>`));
const mapMethods=chapterContent(extraChapters[1],'about');
await emit('about',layout('About this guide','about',`${intro('World guide','About this guide','The source collection, illustration conventions and downloadable references.')}<article class="prose"><h2 id="scope">What the accounts describe</h2><p>The guides describe landscapes, peoples, histories, languages and everyday magic. Naturalist accounts distinguish observations from theories and religious beliefs. Spiritual encounters and many early histories remain uncertain.</p><h2 id="sources">Sources</h2><p>This edition draws together the <a href="https://drive.google.com/drive/folders/126BrWsD3GZ-Qg2oGTjxX3lN_Tp642AXt">public source collection</a>, synchronized on 20 September 2026. Its 36 subject documents are gathered into five guides, with the skies introduced on the home page and map conventions explained here. The complete source snapshot remains in the repository.</p><p>The four new landscape and house illustrations were generated with an image tool from the public descriptions. The seven vector maps were drawn from those descriptions. Local scenery and architectural details are illustrative. Earlier research maps remain in the repository’s historical archive.</p><h2 id="reading-maps">Reading the maps</h2>${mapMethods.html}<h2 id="downloads">Downloads</h2><p>Each Markdown guide includes its full text and image links. Korvar includes all 97 translated examples and 562 dictionary records.</p><ul>${guides.map(g=>`<li><a href="guides/${g.id}.md" download>${esc(g.label)}: complete guide</a></li>`).join('')}</ul><ul><li><a href="data/korvar-lexicon.tsv">Common dictionary (TSV)</a></li><li><a href="data/regional-dictionary.tsv">Regional dictionary (TSV)</a></li><li><a href="data/korvar-examples.tsv">Translated examples (TSV)</a></li><li><a href="lexicon.json">Lexicon (JSON)</a></li><li><a href="maps.json">Source atlas index (JSON)</a></li><li><a href="catalog.json">Source document catalog (JSON)</a></li><li><a href="PUBLIC-INDEX.txt">Source collection index (text)</a></li><li><a href="reader-index.json">Guide and illustration index (JSON)</a></li></ul><h2 id="accessibility">Reading preferences</h2><p>The guide follows your device’s light or dark appearance until you choose a theme. Printed guides use a light background. The full text, dictionary and illustrations remain available without JavaScript.</p><p>Search and dictionary filtering use JavaScript. Page contents, keyboard focus, scrollable tables and full-size image links support longer reference reading. Each illustration has a description and an explanatory caption.</p></article>`));

const realPages=new Set([...guides.map(g=>g.id),'index','about','search']);
for(const [file,map] of Object.entries(routes)) {
  const name=file.replace('.html','');
  if(realPages.has(name)) continue;
  const page=catalog.find(p=>p.id===name);
  const title=page?.title||({dictionary:'Korvar dictionary',worlds:'Worlds',peoples:'Peoples',cosmology:'Magic and belief',language:'Language',maps:'Maps',reference:'References'}[name]||'Public guide');
  const target=map[''];
  const links=Object.entries(map).filter(([old])=>old).map(([old,destination])=>`<li id="${esc(old)}"><a href="${esc(destination)}">${esc(sourceSections.get(name)?.find(s=>s.oldAnchor===old)?.title||old)}</a></li>`).join('');
  const source=page?`<p><a href="https://github.com/Andeleidun/test-fantasy-world/blob/main/content/public/${page.file}">Source document</a></p>`:'';
  await emit(name,layout(title,'',`${intro('World guide',title,'This material is now part of a complete guide.')}<p><a class="continue-link" href="${target}">Continue to the guide</a></p>${source}<ul class="compatibility-links">${links}</ul><script id="redirect-destinations" type="application/json">${JSON.stringify(map).replaceAll('<','\\u003c')}</script><script src="assets/redirect.js"></script>`,{canonical:target,compatibility:true}));
}
await writeFile(resolve(out,'search-index.json'),JSON.stringify(searchIndex));
await writeFile(resolve(out,'reader-index.json'),JSON.stringify({guides,figures,coverage},null,2));
await writeFile('content/reader/coverage.json',JSON.stringify(coverage,null,2)+'\n');
await writeFile(resolve(out,'redirects.json'),JSON.stringify(routes));
await emit('404',layout('Page not found','',`${intro('404','Page not found','The address may have changed or be incomplete.')}<p><a href="index.html">Return to the guide</a></p>`).replace('<head>','<head><base href="/test-fantasy-world/">'));
console.log(`Built ${guides.length} complete guides, ${figures.length} inline figures, ${lexicon.length} dictionary records and ${coverage.length} source destinations.`);
