import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir, stat } from 'node:fs/promises';
import { resolve } from 'node:path';

test('all generated internal links and fragments resolve under the project prefix', async () => {
  const pages = (await readdir('dist')).filter(file => file.endsWith('.html'));
  for (const file of pages) {
    const html = await readFile(`dist/${file}`, 'utf8');
    const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
    assert.equal(ids.length, new Set(ids).size, `Duplicate ids in ${file}`);
    assert.equal((html.match(/<h1[ >]/g) || []).length, 1, `One h1 in ${file}`);
    for (const [, value] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
      if (/^(https?:|data:)/.test(value)) continue;
      const url = new URL(value.replaceAll('&amp;', '&'), `https://example.test/test-fantasy-world/${file}`);
      assert.ok(url.pathname.startsWith('/test-fantasy-world/'), `Base path lost: ${value} in ${file}`);
      let target = url.pathname.replace('/test-fantasy-world/', '') || 'index.html';
      if (target.endsWith('/')) target += 'index.html';
      assert.ok((await stat(resolve('dist', target))).isFile(), `Missing ${target}`);
      if (url.hash && target.endsWith('.html')) {
        const body = await readFile(resolve('dist', target), 'utf8');
        assert.ok(body.includes(`id="${decodeURIComponent(url.hash.slice(1))}"`), `Missing ${value} in ${file}`);
      }
    }
  }
});

test('the publication is worldbuilding only and search references exist', async () => {
  const catalog = JSON.parse(await readFile('content/public/catalog.json', 'utf8'));
  for (const page of catalog) {
    const text = await readFile(`content/public/${page.file}`, 'utf8');
    assert.doesNotMatch(text, /\b(Andel|Marrak|Soren|Megan|Adair|Lacy|Shaloss|Vesheeth)\b/i, page.id);
    assert.notEqual(page.category, 'story');
  }
  const index = JSON.parse(await readFile('dist/search-index.json', 'utf8'));
  assert.ok(index.some(item => item.title === 'hamarkor'));
  for (const item of index) {
    const [file, hash] = item.href.split('#');
    const html = await readFile(`dist/${file}`, 'utf8');
    if (hash) assert.ok(html.includes(`id="${hash}"`), item.href);
  }
});

test('the public edition owns publication inputs and retains important distinctions', async () => {
  const catalog = JSON.parse(await readFile('content/public/catalog.json', 'utf8'));
  const ids = catalog.map(page => page.id);
  assert.equal(ids.length, new Set(ids).size);
  const oldCatalog = JSON.parse(await readFile('content/catalog.json', 'utf8'));
  for (const page of oldCatalog) assert.ok(ids.includes(page.id), `Lost route: ${page.id}`);
  for (const page of catalog) {
    const source = await readFile(`content/public/${page.file}`, 'utf8');
    assert.ok(source.startsWith('# ' + page.title + '\n'));
    for (const [, href] of source.matchAll(/\]\(([^)]+)\)/g)) {
      if (!/^https?:/.test(href)) assert.ok((await stat(resolve('content/public', href.split('#')[0]))).isFile(), href);
    }
    const html = await readFile(`dist/${page.id}.html`, 'utf8');
    assert.ok(html.includes(`/blob/main/content/public/${page.file}`));
    assert.doesNotMatch(html, /Supersession record|Next simulation step|The user selected|Decision \d+:|Countless ways to live/);
  }
  const search = await readFile('dist/search-index.json', 'utf8');
  assert.doesNotMatch(search, /Supersession record|Next simulation step|The user selected|controlled late-parent model/);
  const dwarf = await readFile('content/public/dverghamar-reference.md', 'utf8');
  assert.match(dwarf, /target envelope, not a climate result/);
  assert.match(dwarf, /Thal catastrophe occurred on Erde/);
  const people = await readFile('content/public/hamarkorar.md', 'utf8');
  assert.match(people, /five species and a deep-massif subspecies/);
  assert.match(people, /Hamkor.*proposed/);
  const files = await readdir('dist');
  assert.ok(!files.includes('README.md') && !files.includes('SOURCES.md'));
});

test('public dictionary downloads match the displayed edition and preserve forms', async () => {
  const words = JSON.parse(await readFile('content/public/lexicon.json', 'utf8'));
  const original = JSON.parse(await readFile('content/lexicon.json', 'utf8'));
  assert.deepEqual(words.map(w => [w.lemma,w.pos,w.parts]), original.map(w => [w.lemma,w.pos,w.parts]));
  const download = await readFile('dist/data/korvar-lexicon.tsv', 'utf8');
  assert.equal(download, await readFile('content/public/data/korvar-lexicon.tsv', 'utf8'));
  const tsv = download.trimEnd().split('\n');
  assert.equal(tsv.length, words.length + 1);
  const columns = tsv.shift().split('\t');
  tsv.forEach((line,i) => assert.deepEqual(line.split('\t'), columns.map(key => words[i][key] || '')));
  const regional = (await readFile('dist/data/regional-dictionary.tsv', 'utf8')).trimEnd().split('\n').slice(1);
  for (const row of regional) {
    const [lemma,pos,meaning] = row.split('\t');
    assert.equal(meaning, words.find(w => w.lemma === lemma && w.pos === pos)?.meaning);
  }
  const examples = await readFile('dist/data/korvar-examples.tsv', 'utf8');
  assert.equal(examples.trimEnd().split('\n').length, 99);
  assert.equal(examples, await readFile('content/public/data/korvar-examples.tsv', 'utf8'));
});

test('public Erde uses its own identity while naming proposals remain authorial', async () => {
  const forbidden = /\b(?:Earth|Africa\w*|America\w*|Europe\w*|Asia\w*|Pacific|Atlantic|Bering\w*|Sunda|Flores|Luzon|Papua\w*|Sahul|Neanderthal\w*|Denisovan\w*|erectus|sapiens|Proposal 4)\b/i;
  for (const file of ['erde.md','erde-reference.md','erde-atlas.md','thals.md','map-methods.md']) {
    const source = await readFile(`content/public/${file}`, 'utf8');
    assert.doesNotMatch(source, forbidden, file);
    assert.doesNotMatch(source, /\b(?:Oratha|Veyra|Tavren|Selvara|Maruun|Ilyra|Erden)\b/, `Unapproved name in ${file}`);
  }
  const maps = JSON.parse(await readFile('content/public/maps.json', 'utf8'));
  for (const map of maps.filter(m => m.world === 'Erde')) {
    assert.doesNotMatch(map.title + map.description + map.reading, forbidden);
    const current = await readFile(`dist/assets/maps/${map.stem}.svg`, 'utf8');
    assert.doesNotMatch(current, forbidden, map.stem);
    assert.equal(current, await readFile(`dist/assets/maps/${map.legacyStem}.svg`, 'utf8'));
  }
  const index = JSON.parse(await readFile('dist/search-index.json', 'utf8'));
  for (const item of index.filter(i => /^(erde|thals|map-methods)/.test(i.href))) assert.doesNotMatch(item.title + item.text, forbidden, item.href);
  await assert.rejects(stat('dist/data/erde-reference-locations.csv'));
});
