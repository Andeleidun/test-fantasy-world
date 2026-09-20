import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { catalog, legacyWordAnchor, wordAnchor, wordKey } from '../scripts/public-edition.mjs';

import { guides, readerFiles, figures, routes, coverage } from '../scripts/reader-edition.mjs';

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

test('five guides cover every source and old article routes remain reachable', async () => {
  assert.equal(guides.length, 5);
  assert.equal(catalog.length, 37);
  assert.deepEqual([...new Set(coverage.map(item => item.source))].sort(), catalog.map(item => item.file).sort());
  const publishedRoutes = await json('dist/redirects.json');
  for (const [file, destinations] of Object.entries(publishedRoutes)) {
    assert.ok(await readFile(`dist/${file}`, 'utf8'));
    for (const destination of Object.values(destinations)) {
      const [target, hash] = destination.split('#');
      const html = await readFile(`dist/${target}`, 'utf8');
      if (hash) assert.ok(html.includes(`id="${hash}"`), `${file} -> ${destination}`);
    }
  }
  for (const item of coverage) {
    const [file, anchor] = item.destination.split('#');
    const html = await readFile(`dist/${file}`, 'utf8');
    assert.ok(html.includes(`id="${anchor}"`), JSON.stringify(item));
    if (item.status === 'merged') assert.ok(item.reason);
  }
  const home = await readFile('dist/index.html', 'utf8');
  for (const guide of guides) {
    assert.ok(home.includes(`href="${guide.id}.html"`));
    const html = await readFile(`dist/${guide.id}.html`, 'utf8');
    assert.equal((html.match(/class="guide-chapter"/g) || []).length, guide.chapters.length);
    assert.doesNotMatch(html, /Related reading|Back to undefined|Map illustrations are awaiting|text only/);
  }
});

test('only reviewed reader assets and public datasets are deployed', async () => {
  assert.deepEqual((await walk('dist/assets')).sort(), readerFiles.map(file => `dist/assets/${file}`).sort());
  for (const file of ['catalog.json', 'maps.json', 'lexicon.json', 'PUBLIC-INDEX.txt', 'data/korvar-lexicon.tsv', 'data/regional-dictionary.tsv', 'data/korvar-examples.tsv']) {
    assert.deepEqual(await readFile(`dist/${file}`), await readFile(`content/public/${file}`), file);
  }
  const all = await walk('dist');
  assert.ok(all.every(file => !/assets\/maps\/|\/docs\/|provenance|SOURCES|erde-reference-locations/.test(file)));
  const search = await readFile('dist/search-index.json', 'utf8');
  assert.doesNotMatch(search, /0\.1776 AU|38\.65 Earth days|23\.2 days|controlled late-parent model|rapid planetary return|manufactur(?:e|ing) new souls/i);
  const home = await readFile('dist/index.html', 'utf8');
  assert.doesNotMatch(home, /scenario targets|system architecture|biological models|unresolved gates/);
});

test('every atlas subject has a reviewed inline map; every reader figure appears in its guide', async () => {
  const maps = await json('content/public/maps.json');
  assert.equal(maps.length, 13);
  assert.equal(figures.length, 12);
  for (const map of maps) {
    const figure = figures.find(item => item.codes?.includes(map.code));
    assert.ok(figure, map.code);
    const html = await readFile(`dist/${figure.guide}.html`, 'utf8');
    assert.ok(html.includes(`id="${map.code.toLowerCase()}"`));
    assert.ok(html.includes(`src="assets/${figure.file}"`));
  }
  for (const figure of figures) {
    const html = await readFile(`dist/${figure.guide}.html`, 'utf8');
    assert.ok(html.includes(`id="figure-${figure.id}"`));
    assert.ok(figure.alt.length > 25 && figure.caption.length > 25);
    assert.equal((html.match(new RegExp(`id="figure-${figure.id}"`, 'g')) || []).length, 1);
  }
});

test('dictionary identity survives omissions and all language datasets agree', async () => {
  const words = await json('content/public/lexicon.json');
  const original = await json('content/lexicon.json');
  const legacy = await json('content/dictionary-anchors.json');
  assert.equal(words.length, 562);
  assert.equal(new Set(words.map(wordKey)).size, words.length);
  assert.equal(new Set(words.map(wordAnchor)).size, words.length);
  const dictionary = await readFile('dist/korvar.html', 'utf8');
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

test('complete Markdown guides have working local links and retain every translated example', async () => {
  const { stat } = await import('node:fs/promises');
  const { resolve, dirname } = await import('node:path');
  for (const guide of guides) {
    const file=`dist/guides/${guide.id}.md`;
    const source=await readFile(file,'utf8');
    assert.equal(source,await readFile(`guides/${guide.id}.md`,'utf8'));
    for (const [,href] of source.matchAll(/\]\(([^)]+)\)/g)) {
      if (/^https?:/.test(href)) continue;
      const [path,hash]=href.split('#');
      const target=path?resolve(dirname(file),path):resolve(file);
      assert.ok((await stat(target)).isFile(),`${file}: ${href}`);
      if (hash) {
        const body=await readFile(target,'utf8');
        assert.ok(body.includes(`id="${hash}"`),`${file}: ${href}`);
      }
    }
  }
  const lines=(await readFile('content/public/data/korvar-examples.tsv','utf8')).trimEnd().split('\n');
  const columns=lines.shift().split('\t');
  const gnomes=await readFile('guides/merenval.md','utf8');
  assert.match(gnomes,/body is built from differentiated fungal or fungus-like tissues/);
  assert.match(gnomes,/grown across centuries into a city-scale house/);
  const source=await readFile('guides/korvar.md','utf8');
  for (const line of lines) {
    const values=line.split('\t');
    for (const column of ['text','translation']) {
      const i=columns.indexOf(column);
      assert.ok(i>=0,columns.join(','));
      assert.ok(source.includes(values[i]),`${values[0]}: ${column}`);
    }
  }
});
