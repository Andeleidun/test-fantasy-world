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
  const catalog = JSON.parse(await readFile('content/catalog.json', 'utf8'));
  for (const page of catalog) {
    const text = await readFile(`content/${page.file}`, 'utf8');
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
