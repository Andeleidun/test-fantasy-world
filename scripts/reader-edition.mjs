import { readFile } from 'node:fs/promises';
import { catalog, articleSources, publicLink } from './public-edition.mjs';

export const guides = JSON.parse(await readFile('content/reader/guides.json', 'utf8'));
export const edits = JSON.parse(await readFile('content/reader/edits.json', 'utf8'));
export const figures = JSON.parse(await readFile('content/reader/figures.json', 'utf8'));
const previous = JSON.parse(await readFile('content/section-anchors.json', 'utf8'));
const maps = JSON.parse(await readFile('content/public/maps.json', 'utf8'));
export const slug = value => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section';
export const routes = {};
export const coverage = [];
export const sourceSections = new Map();
export const extraChapters = [
  { id:'skies', title:'The worlds and their skies', sources:['stellar-system-reference'], guide:'index' },
  { id:'reading-maps', title:'Reading the maps', sources:['map-methods'], guide:'about' },
];
const chapterList = [...guides.flatMap(guide => guide.chapters.map(chapter => ({ ...chapter, guide: guide.id }))), ...extraChapters];
const rights = /\n*All original project IP remains the author’s\. Public documentation grants no license or right to reuse this work\.\s*$/;
export function cleanText(value) {
  let text = value.replace(rights, '').replace(/^- \[[^\n]+\]\([^\n]+\)\s*$/gm, '');
  text = text.replace(/<!-- guide-figure: ([\w-]+) -->[\s\S]*?<!-- \/guide-figure -->/g, (block, id) => {
    if (!figures.some(figure => figure.id === id)) throw new Error(`Unknown source figure: ${id}`);
    return '';
  });
  for (const [from,to] of Object.entries(edits.textReplacements)) text = text.replaceAll(from,to);
  return text.trim();
}
for (const chapter of chapterList) for (const id of chapter.sources) {
  const page = catalog.find(page => page.id === id);
  if (!page) throw new Error(`Unknown source ${id}`);
  const source = articleSources.get(page.file).replace(/^# [^\n]+\n+/, '').replace(rights, '');
  const matches = [...source.matchAll(/^(#{2,6}) (.+)$/gm)];
  const counts = new Map();
  const sections = [{ oldAnchor:'', title:page.title, level:2, text:source.slice(0,matches[0]?.index ?? source.length), anchor:chapter.id }];
  for (let i=0;i<matches.length;i++) {
    const match = matches[i], base = slug(match[2]), n=(counts.get(base)||0)+1;
    counts.set(base,n);
    const atlas = maps.find(map => map.guide === page.file && match[2].startsWith(map.code+' ·'));
    const oldAnchor = atlas ? atlas.code.toLowerCase() : base+(n>1?`-${n}`:'');
    const anchor = atlas ? oldAnchor : id===chapter.guide ? oldAnchor : `${id}--${oldAnchor}`;
    sections.push({ oldAnchor, title:match[2], level:match[1].length+1, text:source.slice(match.index+match[0].length,matches[i+1]?.index ?? source.length), anchor });
  }
  routes[`${id}.html`] = { '':`${chapter.guide}.html#${chapter.id}` };
  for (const section of sections) {
    const key=`${id}#${section.oldAnchor}`, omission=edits.omit[key];
    const destination = omission ? omission.target.replace('#','.html#') : `${chapter.guide}.html#${section.anchor}`;
    routes[`${id}.html`][section.oldAnchor] = destination;
    section.text = cleanText(edits.replace[key] ?? section.text);
    section.omitted = Boolean(omission);
    section.sourceId=id;
    section.guide=chapter.guide;
    section.chapter=chapter.id;
    coverage.push({source:page.file,sourceAnchor:section.oldAnchor,destination,status:omission?'merged':edits.replace[key]?'updated':'included',...(omission?{reason:omission.reason}:{})});
  }
  for (const [old,target] of Object.entries(previous[id]||{})) {
    if (!routes[`${id}.html`][target]) throw new Error(`Missing old alias destination ${id}#${target}`);
    routes[`${id}.html`][old]=routes[`${id}.html`][target];
  }
  sourceSections.set(id,sections);
}
// Utility pages from the earlier reader now lead to a complete guide or its index.
routes['README.html']={'':'index.html#guides','documents':'index.html#guides','data-and-indexes':'about.html#downloads'};
coverage.push({source:'README.md',sourceAnchor:'',destination:'index.html#guides',status:'updated',reason:'The five-guide index replaces the document catalog. Source data links are retained under About/downloads.'});
for (const [file,target] of Object.entries({worlds:'index.html#guides',peoples:'index.html#peoples',cosmology:'magic.html',language:'korvar.html',maps:'index.html#maps',reference:'index.html#guides',dictionary:'korvar.html#dictionary-section'})) routes[`${file}.html`]={'':target};
export function readerLink(href) {
  const local=publicLink(href);
  if (/^(?:https?:|mailto:|#)/.test(local)) return local;
  const [file,fragment='']=local.split('#');
  const map=routes[file];
  if (!map) return local;
  if (file==='dictionary.html' && fragment) return `korvar.html#${fragment}`;
  if (fragment && !map[fragment] && guides.some(guide => file===`${guide.id}.html`)) return local;
  return map[fragment] || map[''];
}
export const readerFiles = ['app.js','styles.css','theme.js','favicon.svg','Stavmark.svg','redirect.js',...figures.filter(f=>f.file!=='Stavmark.svg').map(f=>f.file)];
