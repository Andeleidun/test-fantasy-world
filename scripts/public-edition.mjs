import { readFile } from 'node:fs/promises';

export const sourceManifest = JSON.parse(await readFile('content/public-sync.json', 'utf8'));
export const catalog = JSON.parse(await readFile('content/public/catalog.json', 'utf8'));
export const articleSources = new Map();
for (const page of catalog) {
  const source = await readFile(`content/public/${page.file}`, 'utf8');
  const title = source.match(/^# (.+)\r?$/m)?.[1];
  if (!title) throw new Error(`Missing article title: ${page.file}`);
  page.title = title;
  const correction = sourceManifest.displayCorrections.find(item => item.file === page.file);
  if (correction?.description) page.description = correction.description;
  articleSources.set(page.file, source);
}

const routes = new Map(catalog.map(page => [page.file, `${page.id}.html`]));
const sourceLinks = new Map(sourceManifest.files.map(file => {
  const relative = file.path.replace('content/public/', '');
  const target = relative === 'lexicon.json' ? 'dictionary.html' : routes.get(relative) || relative;
  return [file.sourceId, target];
}));

export function publicLink(href) {
  if (!href) return href;
  const drive = href.match(/^https:\/\/(?:drive|docs)\.google\.com\/(?:file|document)\/d\/([^/?#]+)/);
  if (drive && sourceLinks.has(drive[1])) return sourceLinks.get(drive[1]);
  return href.replace(/^([A-Za-z-]+)\.md(?=#|$)/, '$1.html').replace(/^\.\.\/\.\.\/assets\//, 'assets/');
}

export const readerAssets = ['app.js', 'styles.css', 'theme.js', 'favicon.svg', 'Stavmark.svg'];
const previousAnchors = JSON.parse(await readFile('content/dictionary-anchors.json', 'utf8'));
export const wordKey = word => [word.lemma, word.pos, word.parts || ''].join('\t');
// Encoding the complete lexical key avoids collisions between accented forms and homographs.
export const wordAnchor = word => `lex-${Buffer.from(wordKey(word)).toString('base64url')}`;
export const legacyWordAnchor = word => previousAnchors[wordKey(word)] === undefined ? null : `word-${previousAnchors[wordKey(word)]}`;

export const related = {
  erde: ['erde-reference', 'erde-history-full-reference', 'goblins', 'thals', 'erde-atlas'],
  dverghamar: ['hamarkorar', 'evolution-reference', 'thals', 'jotuns', 'dverghamar-reference', 'dverghamar-atlas'],
  merenval: ['elves', 'gnomes', 'orcs', 'merenval-reference'],
  gnomes: ['gnomes-full-reference', 'merenval'],
  jotuns: ['jotuns-full-reference', 'dverghamar'],
  'erde-reference': ['erde-history-full-reference', 'erde-atlas'],
  'language-writing': ['language-examples', 'korvar'],
};
