import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { catalog, readerAssets, legacyWordAnchor, wordAnchor, wordKey } from '../scripts/public-edition.mjs';

const json = async path => JSON.parse(await readFile(path, 'utf8'));
const walk = async dir => (await Promise.all((await readdir(dir, { withFileTypes: true })).map(async entry => {
  const path = `${dir}/${entry.name}`;
  return entry.isDirectory() ? walk(path) : [path];
}))).flat();

test('all 44 public sources retain their complete synchronized bytes', async () => {
  const manifest = await json('content/public-sync.json');
  assert.equal(manifest.files.length, 44);
  assert.equal(new Set(manifest.files.map(file => file.sourceId)).size, 44);
  assert.equal(new Set(manifest.files.map(file => file.path)).size, 44);
  assert.deepEqual((await walk('content/public')).sort(), manifest.files.map(file => file.path).sort());
  for (const file of manifest.files) {
    const bytes = await readFile(file.path);
    assert.equal(bytes.length, file.sizeBytes, file.path);
    assert.equal(createHash('sha256').update(bytes).digest('hex'), file.sha256, file.path);
    assert.ok(file.sourceUrl.includes(file.sourceId));
    assert.ok(!Number.isNaN(Date.parse(file.modifiedTime)));
  }
});

test('every source article and category is reachable; existing article routes survive', async () => {
  const publicMarkdown = (await readdir('content/public')).filter(file => file.endsWith('.md')).sort();
  assert.equal(catalog.length, 37);
  assert.deepEqual(catalog.map(page => page.file).sort(), publicMarkdown);
  assert.equal(new Set(catalog.map(page => page.id)).size, catalog.length);
  for (const page of await json('content/catalog.json')) assert.ok(catalog.some(current => current.id === page.id), page.id);
  for (const page of catalog) {
    const html = await readFile(`dist/${page.id}.html`, 'utf8');
    assert.ok(html.includes(`/blob/main/content/public/${page.file}`));
    assert.doesNotMatch(html, /Back to undefined|\/file\/d\//);
    const category = await readFile(`dist/${page.category}.html`, 'utf8');
    assert.ok(category.includes(`href="${page.id}.html"`));
  }
  const title = 'Gnomes: a comparative account of body, house, kinship and craft';
  assert.equal(catalog.find(page => page.id === 'gnomes-full-reference').title, title);
  assert.ok((await readFile('dist/gnomes-full-reference.html', 'utf8')).includes(`<h1>${title}</h1>`));
});

test('only reviewed reader assets and public datasets are deployed', async () => {
  assert.deepEqual((await walk('dist/assets')).sort(), readerAssets.map(file => `dist/assets/${file}`).sort());
  for (const file of ['catalog.json', 'maps.json', 'lexicon.json', 'PUBLIC-INDEX.txt', 'data/korvar-lexicon.tsv', 'data/regional-dictionary.tsv', 'data/korvar-examples.tsv']) {
    assert.deepEqual(await readFile(`dist/${file}`), await readFile(`content/public/${file}`), file);
  }
  const all = await walk('dist');
  assert.ok(all.every(file => !/\/maps\/|\/docs\/|provenance|SOURCES|erde-reference-locations/.test(file)));
  const search = await readFile('dist/search-index.json', 'utf8');
  assert.doesNotMatch(search, /0\.1776 AU|38\.65 Earth days|23\.2 days|controlled late-parent model|rapid planetary return|manufactur(?:e|ing) new souls/i);
  const home = await readFile('dist/index.html', 'utf8');
  assert.doesNotMatch(home, /scenario targets|system architecture|biological models|unresolved gates/);
});

test('thirteen atlas subjects resolve to text without withdrawn artwork', async () => {
  const maps = await json('content/public/maps.json');
  assert.equal(maps.length, 13);
  for (const map of maps) {
    assert.equal(map.stem, undefined);
    const html = await readFile(`dist/${map.guide.replace('.md', '.html')}`, 'utf8');
    assert.ok(html.includes(`id="${map.code.toLowerCase()}"`), map.code);
    assert.doesNotMatch(html, /assets\/maps\/|Open full-size map/);
  }
});

test('dictionary identity survives omissions and all language datasets agree', async () => {
  const words = await json('content/public/lexicon.json');
  const original = await json('content/lexicon.json');
  const legacy = await json('content/dictionary-anchors.json');
  assert.equal(words.length, 562);
  assert.equal(new Set(words.map(wordKey)).size, words.length);
  assert.equal(new Set(words.map(wordAnchor)).size, words.length);
  const dictionary = await readFile('dist/dictionary.html', 'utf8');
  for (const word of words) {
    const oldIndex = original.findIndex(old => wordKey(old) === wordKey(word));
    if (oldIndex >= 0) assert.equal(legacyWordAnchor(word), `word-${oldIndex}`);
    assert.ok(dictionary.includes(`id="${wordAnchor(word)}"`));
    assert.ok(dictionary.includes(`id="${legacyWordAnchor(word)}"`));
  }
  const currentKeys = new Set(words.map(wordKey));
  for (const [key, index] of Object.entries(legacy)) if (!currentKeys.has(key)) assert.ok(!dictionary.includes(`id="word-${index}"`), key);
  const tsv = (await readFile('dist/data/korvar-lexicon.tsv', 'utf8')).trimEnd().split('\n');
  const columns = tsv.shift().split('\t');
  assert.equal(tsv.length, words.length);
  tsv.forEach((row, i) => assert.deepEqual(row.split('\t'), columns.map(key => words[i][key] || '')));
  const regional = (await readFile('dist/data/regional-dictionary.tsv', 'utf8')).trimEnd().split('\n').slice(1);
  assert.equal(regional.length, words.length);
  for (const row of regional) {
    const [lemma, pos, meaning] = row.split('\t');
    assert.equal(meaning, words.find(word => word.lemma === lemma && word.pos === pos)?.meaning);
  }
  const examples = (await readFile('dist/data/korvar-examples.tsv', 'utf8')).trimEnd().split('\n').slice(1);
  assert.equal(examples.length, 97);
  assert.equal(new Set(examples.map(row => row.split('\t')[0])).size, 97);
});

test('public edition retains current substantive distinctions', async () => {
  const read = name => readFile(`content/public/${name}.md`, 'utf8');
  assert.match(await read('thals'), /native Hamarkorar are not descended from the refugees/);
  assert.match(await read('hamarkorar'), /five species and a deep-massif subspecies/);
  assert.match(await read('elves'), /four major traditions/);
  assert.match(await read('elves'), /not a verified explanation of their origins/);
  assert.match(await read('goblins'), /acquire useful features, diminish them, or lose them altogether/);
  assert.match(await read('gnomes-full-reference'), /not be confused with the Otherworld rooms/);
  assert.match(await read('cosmology-reference'), /Failure to reach someone does not disclose that person’s fate/);
  assert.match(await read('orcs'), /walking, running or bounding along the bottom/);
});
