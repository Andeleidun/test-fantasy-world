// Run deliberately before reviewing and uploading edited public sources.
// The site renders these same figures through figures.json, once per guide.
import { readFile, writeFile } from 'node:fs/promises';
const figures = JSON.parse(await readFile('content/reader/figures.json', 'utf8'));
const slug = value => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const base = 'https://andeleidun.github.io/test-fantasy-world/assets/';
const sources = new Map();
for (const figure of figures) {
  const [source, section] = figure.after?.split('#') || [figure.guide, ''];
  if (!sources.has(source)) sources.set(source, []);
  sources.get(source).push({ figure, section });
}
for (const [source, entries] of sources) {
  const path = `content/public/${source}.md`;
  let text = (await readFile(path, 'utf8')).replace(/\n*<!-- guide-figure: [\w-]+ -->[\s\S]*?<!-- \/guide-figure -->\n*/g, '\n\n');
  for (const { figure, section } of entries) {
    const block = `\n\n<!-- guide-figure: ${figure.id} -->\n![${figure.alt}](${base}${figure.file})\n\n${figure.caption}\n<!-- /guide-figure -->\n\n`;
    const headings = [...text.matchAll(/^## (.+)$/gm)];
    const index = section ? headings.findIndex(h => slug(h[1]) === section || h[1].startsWith(section.toUpperCase() + ' ·')) : -1;
    if (section && index < 0) throw new Error(`Missing figure section: ${source}#${section}`);
    const end = section ? headings[index + 1]?.index ?? text.indexOf('\nAll original project IP') : headings[0]?.index;
    if (!(end >= 0)) throw new Error(`Missing insertion point: ${source}`);
    text = text.slice(0, end).trimEnd() + block + text.slice(end).trimStart();
  }
  await writeFile(path, text);
}
console.log(`Embedded ${figures.length} figures in ${sources.size} public sources.`);
